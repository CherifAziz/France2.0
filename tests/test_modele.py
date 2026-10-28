"""Cas analytiques synthétiques : aucun chiffre national dans ces tests."""
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("modele_financier", ROOT / "modele" / "modele.py")
model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(model)


def inputs():
    hyp = {
        "annee_debut": 2027, "annee_fin": 2036,
        "couts_k_eur": {"FPE": {"cout_entree_hors_pension": 40, "cout_moyen_hors_pension": 50}},
        "gvt_individuel_reel": 0, "facteur_transfert_cout": 0.8,
        "indemnite_depart_k_eur": 10, "taux_conservation_consolide": 0.6,
        "fraction_economie_premiere_annee": 1,
    }
    v = {"vivier_id": "V", "versant": "FPE", "etp_base": 100, "taux_departs_annuel": 0.1}
    v.update({f"plafond_reduction_{sc}": 1 for sc in model.SCENARIOS})
    return hyp, {"V": v}


def reform(rid="R1", rate=0.2, order=1, start=2027, duration=1, mode="non_remplacement"):
    r = {"id": rid, "intitule": "Cas synthétique " + rid, "vivier_id": "V", "ordre": order,
         "annee_debut": start, "duree_ans": duration, "invest_duree_ans": 1}
    r.update({"part_" + m: int(m == mode) for m in model.MODES})
    for sc in model.SCENARIOS:
        r[f"taux_{sc}"] = rate
        r.update({f"{key}_{sc}": 0 for key in model.MONEY})
    return r


class ModelTests(unittest.TestCase):
    def run_case(self, reforms, hyp=None, viviers=None):
        default_hyp, default_viviers = inputs()
        return model.run_scenario(hyp or default_hyp, viviers or default_viviers, reforms, "prudent")

    def test_nonreplacement_manual_cashflow_and_sums(self):
        rows, annual, alerts = self.run_case([reform()])
        self.assertEqual([annual[y]["etp_non_remplaces"] for y in (2027, 2028, 2029)], [10, 9, 1])
        self.assertEqual([annual[y]["eco_nette_meur"] for y in (2027, 2028, 2029)], [0.4, 0.76, 0.8])
        self.assertAlmostEqual(rows[0]["cumul_net_5ans"], 3.56)
        self.assertAlmostEqual(rows[0]["cumul_net_10ans"], 7.56)
        self.assertAlmostEqual(annual[2036]["eco_consolidee_apu_meur"], 0.48)
        self.assertEqual(alerts, [])

    def test_two_reforms_share_each_year_departures(self):
        rows, annual, _ = self.run_case([reform(), reform("R2", rate=0.5, order=2)])
        self.assertEqual([r["etp_cible"] for r in rows], [20, 40])
        self.assertAlmostEqual(annual[2027]["etp_non_remplaces"], 10)
        self.assertAlmostEqual(annual[2028]["etp_non_remplaces"], 9)
        self.assertAlmostEqual(annual[2029]["etp_non_remplaces"], 8.1)
        for a in annual.values():
            self.assertLessEqual(a["etp_departs_utilises"], a["etp_departs_disponibles"] + 1e-9)
        self.assertAlmostEqual(sum(r["etp_non_remplaces"] for r in rows), 60)
        self.assertAlmostEqual(sum(r["net_2036"] for r in rows), annual[2036]["eco_nette_meur"])

    def test_future_reform_does_not_shrink_current_departure_capacity(self):
        rows, annual, _ = self.run_case([
            reform("FUTURE", rate=0.5, order=1, start=2035),
            reform("NOW", rate=1, order=2),
        ])
        self.assertEqual([r["etp_cible"] for r in rows], [50, 50])
        self.assertEqual(annual[2027]["etp_non_remplaces"], 10)
        self.assertEqual(rows[0]["net_2027"], 0)
        self.assertEqual(rows[1]["net_2027"], 0.4)

    def test_unrealised_targets_cannot_be_counted_twice(self):
        hyp, viviers = inputs()
        viviers["V"]["taux_departs_annuel"] = 0
        rows, annual, alerts = self.run_case([reform(rate=1), reform("R2", rate=1, order=2)], hyp, viviers)
        self.assertEqual([r["etp_cible"] for r in rows], [100, 0])
        self.assertEqual(sum(r["etp_non_remplaces"] for r in rows), 0)
        self.assertTrue(any("non réalisés" in a for a in alerts))
        self.assertEqual(annual[2036]["eco_nette_meur"], 0)

    def test_vivier_ceiling(self):
        hyp, viviers = inputs()
        viviers["V"]["plafond_reduction_prudent"] = 0.3
        rows, _, alerts = self.run_case([reform(), reform("R2", rate=0.5, order=2)], hyp, viviers)
        self.assertEqual([r["etp_cible"] for r in rows], [20, 10])
        self.assertTrue(any("plafonnée" in a for a in alerts))

    def test_private_transfer_has_provider_cost_in_both_readings(self):
        r = reform(rate=1, mode="transfert")
        r["type_transfert"] = "prive"
        rows, annual, _ = self.run_case([r])
        self.assertEqual(annual[2027]["eco_brute_meur"], 5)
        self.assertEqual(annual[2027]["cout_transferts_meur"], 4)
        self.assertEqual(annual[2027]["eco_nette_meur"], 1)
        self.assertEqual(annual[2027]["eco_consolidee_apu_meur"], -1)
        self.assertEqual(rows[0]["etp_postes_apu_en_moins"], 100)

    def test_public_transfer_is_not_a_national_job_reduction(self):
        hyp, viviers = inputs()
        hyp["facteur_transfert_cout"] = 1
        r = reform(rate=1, mode="transfert")
        r.update({"type_transfert": "public", "taux_conservation_transfert": 0.6,
                  "etp_destination_par_etp_transfere": 1, "part_cout_transfert_charge_source": 0})
        rows, annual, _ = self.run_case([r], hyp, viviers)
        self.assertEqual(rows[0]["etp_postes_en_moins"], 100)
        self.assertEqual(rows[0]["etp_postes_apu_en_moins"], 0)
        self.assertEqual(annual[2027]["etp_recrutements_publics_destination"], 100)
        self.assertEqual(annual[2027]["eco_nette_meur"], 5)
        self.assertEqual(annual[2027]["eco_consolidee_apu_meur"], 0)

    def test_public_transfer_productivity_and_source_financing(self):
        r = reform(rate=1, mode="transfert")
        r.update({"type_transfert": "public", "taux_conservation_transfert": 0.6,
                  "etp_destination_par_etp_transfere": 0.8, "part_cout_transfert_charge_source": 0.5})
        rows, annual, _ = self.run_case([r])
        self.assertAlmostEqual(rows[0]["etp_postes_apu_en_moins"], 20)
        self.assertEqual(annual[2027]["eco_nette_meur"], 3)
        self.assertAlmostEqual(annual[2027]["eco_consolidee_apu_meur"], 0.6)

    def test_redeployment_preserves_payroll_and_national_headcount(self):
        rows, annual, _ = self.run_case([reform(rate=1, mode="redeploiement")])
        self.assertEqual(rows[0]["etp_redeployes"], 100)
        self.assertEqual(rows[0]["etp_postes_apu_en_moins"], 0)
        self.assertEqual(annual[2036]["eco_brute_meur"], 0)

    def test_indemnified_suppression_uses_incumbent_cost(self):
        _, annual, _ = self.run_case([reform(rate=0.1, mode="suppression_indemnisee")])
        self.assertEqual(annual[2027]["eco_brute_meur"], 0.5)
        self.assertEqual(annual[2027]["indemnites_meur"], 0.1)
        self.assertAlmostEqual(annual[2027]["eco_nette_meur"], 0.4)

    def test_gvt_is_cohort_based_and_capped(self):
        hyp, viviers = inputs()
        hyp["gvt_individuel_reel"] = 0.1
        _, annual, _ = self.run_case([reform(rate=0.1)], hyp, viviers)
        for y, expected in ((2027, 0.4), (2028, 0.44), (2029, 0.484), (2030, 0.5), (2036, 0.5)):
            self.assertAlmostEqual(annual[y]["eco_brute_meur"], expected)

    def test_half_year_convention_does_not_halve_later_stock(self):
        hyp, viviers = inputs()
        hyp["fraction_economie_premiere_annee"] = 0.5
        _, annual, _ = self.run_case([reform(rate=0.1)], hyp, viviers)
        self.assertEqual(annual[2027]["eco_brute_meur"], 0.2)
        self.assertEqual(annual[2028]["eco_brute_meur"], 0.4)

    def test_half_year_operating_benefit_follows_effective_completion(self):
        hyp, viviers = inputs()
        hyp["fraction_economie_premiere_annee"] = 0.5
        r = reform(rate=0.1)
        r["eco_fonct_meur_prudent"] = 2
        _, annual, _ = self.run_case([r], hyp, viviers)
        self.assertEqual(annual[2027]["eco_fonctionnement_meur"], 1)
        self.assertEqual(annual[2028]["eco_fonctionnement_meur"], 2)

    def test_first_year_investment_is_not_lost(self):
        r = reform(rate=0)
        r.update({"invest_meur_prudent": 9, "invest_duree_ans": 3})
        rows, annual, _ = self.run_case([r])
        self.assertEqual([annual[y]["invest_meur"] for y in (2027, 2028, 2029, 2030)], [3, 3, 3, 0])
        self.assertEqual(rows[0]["cumul_net_10ans"], -9)

    def test_explicit_pre_horizon_investment_is_disclosed(self):
        r = reform(rate=0)
        r.update({"invest_meur_prudent": 9, "invest_duree_ans": 3, "annee_invest_debut": 2026})
        rows, annual, alerts = self.run_case([r])
        self.assertEqual(rows[0]["invest_avant_horizon_meur"], 3)
        self.assertEqual(rows[0]["cumul_net_10ans"], -6)
        self.assertEqual(rows[0]["cumul_net_horizon_incl_invest_avant_meur"], -9)
        s = model.summary("prudent", rows, annual)
        self.assertEqual(s["invest_total_jusqua_fin_horizon_meur"], 9)
        self.assertEqual(s["cumul_net_10ans_incl_invest_avant_meur"], -9)
        self.assertTrue(any("avant 2027" in a for a in alerts))

    def test_post_horizon_reform_has_no_premature_savings(self):
        rows, annual, alerts = self.run_case([reform(start=2037)])
        self.assertEqual(rows[0]["etp_cible_non_realisee"], 20)
        self.assertEqual(rows[0]["etp_non_remplaces"], 0)
        self.assertEqual(sum(a["eco_nette_meur"] for a in annual.values()), 0)
        self.assertTrue(any("après l'horizon" in a for a in alerts))

    def test_cost_only_reform_and_negative_revenue_are_retained(self):
        r = reform(rate=0)
        r.update({"cout_recurrent_meur_prudent": 2, "effet_recettes_meur_prudent": -1})
        rows, annual, _ = self.run_case([r])
        self.assertEqual(rows[0]["cumul_net_10ans"], -30)
        self.assertEqual(annual[2027]["eco_nette_meur"], -3)

    def test_benefits_follow_actual_reduction_but_costs_follow_deployment(self):
        hyp, viviers = inputs()
        viviers["V"]["taux_departs_annuel"] = 0
        r = reform(rate=1)
        r.update({"eco_fonct_meur_prudent": 2, "cout_recurrent_meur_prudent": 1})
        _, annual, _ = self.run_case([r], hyp, viviers)
        self.assertEqual(annual[2036]["eco_fonctionnement_meur"], 0)
        self.assertEqual(annual[2036]["eco_nette_meur"], -1)

    def test_invalid_and_missing_inputs_are_rejected(self):
        bad_rows = []
        r = reform(); r["part_non_remplacement"] = 0; bad_rows.append(r)
        r = reform(); r["taux_prudent"] = 1.1; bad_rows.append(r)
        r = reform(); del r["invest_meur_prudent"]; bad_rows.append(r)
        r = reform(); r["taux_prudent"] = "nan"; bad_rows.append(r)
        r = reform(); r["taux_prudent"] = "inf"; bad_rows.append(r)
        r = reform(); r["annee_debut"] = 2026; bad_rows.append(r)
        r = reform(mode="transfert"); bad_rows.append(r)
        r = reform(); r["vivier_id"] = "UNKNOWN"; bad_rows.append(r)
        r = reform(); r["duree_ans"] = 1.5; bad_rows.append(r)
        for r in bad_rows:
            with self.subTest(row=r), self.assertRaises(ValueError):
                self.run_case([r])
        with self.assertRaises(ValueError):
            self.run_case([reform(), reform()])
        with self.assertRaises(ValueError):
            self.run_case([reform(), reform("R2", order=1)])

    def test_empty_scenario_and_short_horizon(self):
        hyp, viviers = inputs()
        hyp["annee_fin"] = 2028
        rows, annual, _ = self.run_case([], hyp, viviers)
        self.assertEqual(rows, [])
        s = model.summary("prudent", rows, annual)
        self.assertIsNone(s["cumul_net_5ans_meur"])
        self.assertIsNone(s["postes_en_moins_10ans"])
        self.assertEqual(s["cumul_net_horizon_meur"], 0)

    def test_closed_form_attrition_path(self):
        for departure in (0, 0.05, 0.2, 1):
            for duration in (1, 3, 10):
                hyp, viviers = inputs()
                hyp["annee_fin"] = 2026 + duration
                viviers["V"]["taux_departs_annuel"] = departure
                rows, _, _ = self.run_case([reform(rate=1)], hyp, viviers)
                expected = 100 * (1 - (1 - departure) ** duration)
                with self.subTest(departure=departure, duration=duration):
                    self.assertAlmostEqual(rows[0]["etp_non_remplaces"], expected)

    def test_cli_exports_all_scenarios_with_empty_reform_file(self):
        hyp, viviers = inputs()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            vfile, rfile = path / "viviers.csv", path / "reformes.csv"
            for file, rows, fields in ((vfile, list(viviers.values()), list(viviers["V"])),
                                      (rfile, [], list(reform()))):
                with file.open("w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader(); writer.writerows(rows)
            hyp["fichiers"] = {"viviers": str(vfile), "reformes": str(rfile)}
            hfile = path / "hypotheses.json"
            hfile.write_text(json.dumps(hyp), encoding="utf-8")
            with patch.object(sys, "argv", ["modele.py", "--hyp", str(hfile), "--out", str(path / "resultats")]):
                with contextlib.redirect_stdout(io.StringIO()):
                    model.main()
            files = list((path / "resultats").iterdir())
            self.assertEqual(len(files), 10)
            with (path / "resultats" / "synthese_scenarios.csv").open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 4)
            self.assertEqual(float(rows[0]["cumul_net_10ans_meur"]), 0)

    def test_cli_populated_export_reconciles_to_manual_total(self):
        hyp, viviers = inputs()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            r = reform()
            for file, rows in ((path / "viviers.csv", list(viviers.values())),
                               (path / "reformes.csv", [r])):
                with file.open("w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                    writer.writeheader(); writer.writerows(rows)
            hyp["fichiers"] = {"viviers": str(path / "viviers.csv"), "reformes": str(path / "reformes.csv")}
            hfile = path / "hypotheses.json"
            hfile.write_text(json.dumps(hyp), encoding="utf-8")
            with patch.object(sys, "argv", ["modele.py", "--hyp", str(hfile), "--out", str(path / "resultats")]):
                with contextlib.redirect_stdout(io.StringIO()):
                    model.main()
            with (path / "resultats" / "synthese_scenarios.csv").open(encoding="utf-8", newline="") as f:
                summaries = list(csv.DictReader(f))
            self.assertEqual([float(s["cumul_net_10ans_meur"]) for s in summaries], [7.56] * 4)
            self.assertEqual([float(s["etp_viviers_concernes"]) for s in summaries], [100] * 4)


if __name__ == "__main__":
    unittest.main()
