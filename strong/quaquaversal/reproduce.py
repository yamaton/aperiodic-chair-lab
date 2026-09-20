"""Replay the current research checkpoint, including its expected failures.

Run: uv run --locked python strong/quaquaversal/reproduce.py
This is a finite reproduction command, not an unattended discovery loop.
"""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
PREFIX = 'strong/quaquaversal/'
ARTIFACTS = PREFIX+'artifacts/'

COMMANDS = [
    ['verify_geometry.py'],
    ['polynomial_rules.py'],
    ['periodic_obstruction.py'],
    ['reflected_search.py'],
    ['reflected_controls.py'],
    ['reflected_second_level.py'],
    ['refine_vertices.py'],
    ['refine_panels.py'],
    ['audit_panels.py'],
    ['refine_panels.py','--seed-audit',ARTIFACTS+'panel_audit.json','--output',ARTIFACTS+'panel_refinement_v2.json'],
    ['audit_panels.py','--input',ARTIFACTS+'panel_refinement_v2.json','--output',ARTIFACTS+'panel_audit_v2.json'],
    ['piecewise_search.py'],
    ['piecewise_deeper.py'],
    ['piecewise_periodic_grid.py'],
    ['contact_atlas.py'],
    ['atlas_periodic_reflections.py'],
    ['atlas_stars.py'],
    ['star_language.py'],
    ['closed_stars.py','--sample-level','3','--periodic-level','1'],
    ['closed_stars.py','--sample-level','4','--periodic-level','2'],
    ['closed_contact_atlas.py'],
    ['audit_closed_atlas.py'],
    ['closed_star_language.py'],
    ['audit_star_language.py'],
    ['pointwise_groupoid.py'],
    ['pointwise_groupoid.py','--all','--output',ARTIFACTS+'pointwise_groupoid_all.json'],
    ['audit_pointwise_groupoid.py'],
    ['star_parent_consistency.py'],
    ['parent_star_join.py'],
    ['parent_join_filter.py'],
    ['closed_star_compatibility.py'],
    ['audit_star_compatibility.py'],
    ['parent_external_domains.py'],
    ['audit_external_domains.py'],
    ['parent_neighbor_graph.py'],
    ['parent_star_arc_consistency.py'],
    ['audit_parent_arcs.py'],
    ['parent_boundary_cover.py','--arcs','--output',ARTIFACTS+'parent_boundary_cover_arcs.json'],
    ['parent_cover_star_constraints.py'],
    ['forced_outer_layer.py'],
    ['audit_outer_rejections.py'],
    ['audit_cover_domains.py'],
    ['audit_forced_domains.py','--input',ARTIFACTS+'forced_outer_layer.json',
     '--source',ARTIFACTS+'parent_cover_star_constraints.json','--source-poses',ARTIFACTS+'parent_external_domains.json',
     '--output',ARTIFACTS+'forced_outer_layer_full_audit.json'],
    ['propagate_forced_domains.py'],
    ['audit_forced_domains.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'forced_outer_layer_2.json','--output',ARTIFACTS+'forced_outer_layer_3.json'],
    ['audit_forced_domains.py','--input',ARTIFACTS+'forced_outer_layer_3.json','--source',ARTIFACTS+'forced_outer_layer_2.json',
     '--output',ARTIFACTS+'forced_outer_layer_3_audit.json'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'forced_outer_layer_3.json','--output',ARTIFACTS+'forced_outer_layer_4.json'],
    ['audit_forced_domains.py','--input',ARTIFACTS+'forced_outer_layer_4.json','--source',ARTIFACTS+'forced_outer_layer_3.json',
     '--output',ARTIFACTS+'forced_outer_layer_4_audit.json'],
    ['parent_defect_profiles.py'],
    ['forced_patch_geometry.py'],
    ['audit_forced_geometry.py'],
    ['expanded_arc_consistency.py'],
    ['audit_expanded_arcs.py'],
    ['prepare_forced_seed.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'expanded_arc_seed.json','--output',ARTIFACTS+'forced_after_arcs_1.json'],
    ['audit_forced_domains.py','--input',ARTIFACTS+'forced_after_arcs_1.json','--source',ARTIFACTS+'expanded_arc_seed.json',
     '--output',ARTIFACTS+'forced_after_arcs_1_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'forced_after_arcs_1.json','--output',ARTIFACTS+'expanded_arcs_2.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'expanded_arcs_2.json','--source',ARTIFACTS+'forced_after_arcs_1.json',
     '--output',ARTIFACTS+'expanded_arcs_2_audit.json'],
    ['prepare_forced_seed.py','--input',ARTIFACTS+'expanded_arcs_2.json','--poses-source',ARTIFACTS+'forced_after_arcs_1.json',
     '--output',ARTIFACTS+'expanded_arcs_2_seed.json'],
    ['branch_probe_seed.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'branch_probe_seed.json','--output',ARTIFACTS+'branch_probe_layer_1.json'],
    ['audit_forced_domains.py','--input',ARTIFACTS+'branch_probe_layer_1.json','--source',ARTIFACTS+'branch_probe_seed.json',
     '--output',ARTIFACTS+'branch_probe_layer_1_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'branch_probe_seed.json','--output',ARTIFACTS+'branch_probe_arcs.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'branch_probe_arcs.json','--source',ARTIFACTS+'branch_probe_seed.json',
     '--output',ARTIFACTS+'branch_probe_arcs_audit.json'],
    ['audit_branch_probe.py'],
    ['neighbor_incidence_sat.py'],
    ['incidence_model_geometry.py'],
    ['audit_incidence_collisions.py'],
    ['incidence_sample_exclusions.py'],
    ['audit_incidence_samples.py'],
    ['neighbor_incidence_geometry_sat.py'],
    ['incidence_model_star_seed.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'incidence_model_star_seed.json','--output',ARTIFACTS+'incidence_model_star_extension.json'],
    ['audit_incidence_star_cuts.py'],
    ['neighbor_star_cut_sat.py'],
    ['audit_neighbor_star_cuts.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'neighbor_star_cut_seed.json','--output',ARTIFACTS+'neighbor_star_cut_layer_1.json'],
    ['audit_forced_domains_complete.py','--input',ARTIFACTS+'neighbor_star_cut_layer_1.json','--source',ARTIFACTS+'neighbor_star_cut_seed.json',
     '--output',ARTIFACTS+'neighbor_star_cut_layer_1_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'neighbor_star_cut_layer_1.json','--output',ARTIFACTS+'neighbor_star_cut_arcs.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'neighbor_star_cut_arcs.json','--source',ARTIFACTS+'neighbor_star_cut_layer_1.json',
     '--output',ARTIFACTS+'neighbor_star_cut_arcs_audit.json'],
    ['audit_neighbor_arc_cuts.py'],
    ['verify_neighbor_arc_cut_certificate.py'],
    ['prepare_forced_seed.py','--input',ARTIFACTS+'neighbor_star_cut_arcs.json','--poses-source',ARTIFACTS+'neighbor_star_cut_layer_1.json',
     '--output',ARTIFACTS+'neighbor_star_cut_arc_seed.json'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'neighbor_star_cut_arc_seed.json','--output',ARTIFACTS+'neighbor_star_cut_layer_2.json'],
    ['audit_forced_domains_complete.py','--input',ARTIFACTS+'neighbor_star_cut_layer_2.json','--source',ARTIFACTS+'neighbor_star_cut_arc_seed.json',
     '--output',ARTIFACTS+'neighbor_star_cut_layer_2_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'neighbor_star_cut_layer_2.json','--output',ARTIFACTS+'neighbor_star_cut_arcs_2.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'neighbor_star_cut_arcs_2.json','--source',ARTIFACTS+'neighbor_star_cut_layer_2.json',
     '--output',ARTIFACTS+'neighbor_star_cut_arcs_2_audit.json'],
    ['neighbor_arc_cut_sat.py'],
    ['audit_neighbor_arc_sat.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'neighbor_arc_sat_seed.json','--output',ARTIFACTS+'neighbor_arc_sat_layer_1.json'],
    ['audit_forced_domains_complete.py','--input',ARTIFACTS+'neighbor_arc_sat_layer_1.json','--source',ARTIFACTS+'neighbor_arc_sat_seed.json',
     '--output',ARTIFACTS+'neighbor_arc_sat_layer_1_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'neighbor_arc_sat_layer_1.json','--output',ARTIFACTS+'neighbor_arc_sat_arcs.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'neighbor_arc_sat_arcs.json','--source',ARTIFACTS+'neighbor_arc_sat_layer_1.json',
     '--output',ARTIFACTS+'neighbor_arc_sat_arcs_audit.json'],
    ['compare_arc_oracle.py'],
    ['choice_cut_domains.py'],
    ['audit_choice_cut_domains.py'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'choice_cut_changed_seed.json','--output',ARTIFACTS+'choice_cut_arcs.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'choice_cut_arcs.json','--source',ARTIFACTS+'choice_cut_changed_seed.json',
     '--output',ARTIFACTS+'choice_cut_arcs_audit.json'],
    ['merge_choice_cut_frontier.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'choice_cut_frontier_seed.json','--output',ARTIFACTS+'choice_cut_forced_1.json'],
    ['audit_forced_domains_complete.py','--input',ARTIFACTS+'choice_cut_forced_1.json','--source',ARTIFACTS+'choice_cut_frontier_seed.json',
     '--output',ARTIFACTS+'choice_cut_forced_1_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'choice_cut_forced_1.json','--output',ARTIFACTS+'choice_cut_expanded_arcs_1.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'choice_cut_expanded_arcs_1.json','--source',ARTIFACTS+'choice_cut_forced_1.json',
     '--output',ARTIFACTS+'choice_cut_expanded_arcs_1_audit.json'],
    ['layered_choice_certificate.py'],
    ['verify_layered_choice_certificate.py'],
    ['extend_choice_cut_catalog.py'],
    ['coarse_parent_language.py'],
    ['audit_coarse_parent_language.py'],
    ['refine_coarse_frontier.py'],
    ['audit_coarse_refinement.py'],
    ['propagate_choice_cuts.py'],
    ['audit_choice_cut_pass.py'],
    ['propagate_forced_domains.py','--input',ARTIFACTS+'choice_cut_pass_2.json','--output',ARTIFACTS+'choice_cut_forced_2.json'],
    ['audit_forced_domains_complete.py','--input',ARTIFACTS+'choice_cut_forced_2.json','--source',ARTIFACTS+'choice_cut_pass_2.json',
     '--output',ARTIFACTS+'choice_cut_forced_2_audit.json'],
    ['expanded_arc_consistency.py','--input',ARTIFACTS+'choice_cut_forced_2.json','--output',ARTIFACTS+'choice_cut_expanded_arcs_2.json'],
    ['audit_expanded_arcs.py','--input',ARTIFACTS+'choice_cut_expanded_arcs_2.json','--source',ARTIFACTS+'choice_cut_forced_2.json',
     '--output',ARTIFACTS+'choice_cut_expanded_arcs_2_audit.json'],
    ['audit_coarse_support_domains.py'],
    ['coarse_star_arc_filter.py'],
    ['audit_coarse_star_arcs.py'],
    ['enlarged_sibling_roles.py'],
    ['enlarged_sibling_probe.py'],
    ['audit_enlarged_sibling_probe.py'],
    ['merge_coarse_star_filter.py'],
    ['audit_merged_coarse_frontier.py'],
    ['coarse_star_arc_filter.py','--input',ARTIFACTS+'coarse_arc_frontier_1.json','--input-audit',ARTIFACTS+'coarse_arc_frontier_1_audit.json',
     '--output',ARTIFACTS+'coarse_star_arc_filter_2.json'],
    ['audit_coarse_star_arcs.py','--input',ARTIFACTS+'coarse_star_arc_filter_2.json','--source',ARTIFACTS+'coarse_arc_frontier_1.json',
     '--output',ARTIFACTS+'coarse_star_arc_audit_2.json'],
    ['merge_coarse_star_filter.py','--fine',ARTIFACTS+'coarse_arc_frontier_1.json','--fine-audit',ARTIFACTS+'coarse_arc_frontier_1_audit.json',
     '--poses-source',ARTIFACTS+'coarse_arc_frontier_1.json','--filter',ARTIFACTS+'coarse_star_arc_filter_2.json',
     '--filter-audit',ARTIFACTS+'coarse_star_arc_audit_2.json','--output',ARTIFACTS+'coarse_arc_frontier_2.json'],
    ['audit_merged_coarse_frontier.py','--input',ARTIFACTS+'coarse_arc_frontier_2.json','--output',ARTIFACTS+'coarse_arc_frontier_2_audit.json'],
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit-only',action='store_true',help='Check retained artifacts and hashes without rerunning searches')
    options = parser.parse_args()
    runs = ROOT/'artifacts'/'runs'
    runs.mkdir(exist_ok=True)
    records = []
    for i,args in enumerate([] if options.audit_only else COMMANDS,1):
        command = ['uv','run','--locked','python',PREFIX+args[0],*args[1:]]
        print(f'[{i}/{len(COMMANDS)}] '+ ' '.join(command),flush=True)
        result = subprocess.run(command,cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log = runs/f'{i:02d}_{Path(args[0]).stem}.txt'
        log.write_text(result.stdout)
        records.append(dict(command=command,exit_code=result.returncode,log=str(log.relative_to(ROOT))))
        if result.returncode:
            print(result.stdout,flush=True)
            raise SystemExit(result.returncode)
    checks = 0
    for p in sorted((ROOT/'artifacts').glob('*.json')):
        if p.name in ('reproduction.json','reproduction_hash_audit.json'):
            continue
        data = json.loads(p.read_text())
        for name,expected in data.get('sources',{}).items():
            source = ROOT/name if (ROOT/name).exists() else ROOT/'artifacts'/name
            assert hashlib.sha256(source.read_bytes()).hexdigest() == expected,(p.name,name)
            checks += 1
    def read(name):
        return json.loads((ROOT/'artifacts'/name).read_text())
    assert read('panel_audit.json')['failures']  # Retain the failed first refinement.
    assert not read('panel_audit_v2.json')['failures']
    assert read('reflected_second_level.json')['not_rejected_by_control'] == 0
    assert all(r['witness'] is not None for r in read('piecewise_periodic_grid.json')['results'])
    assert read('contact_atlas.json')['status'] == 'closed'
    assert read('atlas_periodic_reflections.json')['volume_ratio'] == '1'
    assert read('star_language_3_1.json')['periodic_control_uses_only_observed_stars']
    assert read('closed_contact_atlas.json')['status'] == 'closed'
    assert read('closed_contact_audit.json')['dimensions'] == {'0':953,'1':247,'2':91}
    assert read('closed_star_language.json')['status'] == 'closed'
    assert read('closed_star_audit.json')['role_multiplicities'] == {'1':6840}
    assert read('closed_star_audit.json')['periodic_bad_cycle']
    assert read('star_parent_consistency.json')['all_sibling_roles_agree']
    assert read('pointwise_groupoid_audit.json')['families'] == 512
    assert len(read('parent_join_filter.json')['extra_tuples']) == 52485
    assert read('parent_external_domains_audit.json')['survivors'] == 11560
    assert read('parent_arc_audit.json')['status_counts'] == {'survivor':9280,'empty_star_domain':2280}
    assert len(read('parent_boundary_cover_arcs.json')['genuine_parent_witnesses']) == 6840
    assert read('parent_cover_star_constraints.json')['status_counts'] == {'survivor':5984,'rejected':3373}
    assert read('forced_outer_layer.json')['status_counts'] == {'survivor':4035,'rejected':1949}
    assert read('outer_rejection_audit.json')['rejected_covers_checked'] == 1949
    assert read('parent_cover_domain_audit.json')['survivors'] == 5984
    assert read('forced_outer_layer_full_audit.json')['survivors'] == 4035
    assert read('forced_outer_layer_2_audit.json')['survivors'] == 1554
    assert read('forced_outer_layer_3_audit.json')['survivors'] == 1076
    assert read('forced_outer_layer_4_audit.json')['survivors'] == 744
    assert read('forced_geometry_audit.json')['rejected_patches'] == 17
    assert read('expanded_arc_audit.json')['survivors'] == 350
    assert read('expanded_arc_seed.json')['status_counts']['survivor'] == 350
    assert read('forced_after_arcs_1_audit.json')['survivors'] == 315
    assert read('expanded_arcs_2_audit.json')['survivors'] == 246
    assert read('expanded_arcs_2_seed.json')['status_counts']['survivor'] == 246
    assert read('branch_probe_audit.json')['additional_parent_exclusions'] == 0
    assert all(r['status'] == 'sat' for r in read('neighbor_incidence_sat.json')['results'])
    assert read('incidence_sample_audit.json')['overlap_clauses'] == 209371
    assert all(r['status'] == 'sat' for r in read('neighbor_incidence_geometry_sat.json')['results'])
    assert read('incidence_star_cuts.json')['assignment_rejections'] == 6
    assert read('incidence_star_cuts.json')['direct_parent_exclusions'] == 0
    assert read('neighbor_star_cut_initial_failure.json')['exit_code'] == 1
    assert read('neighbor_star_cut_audit.json')['new_cuts'] == 117
    assert read('neighbor_star_cut_audit.json')['direct_parent_exclusions'] == 0
    assert all(r['status'] == 'sat_passes_neighbor_star_test' for r in read('neighbor_star_cut_sat.json')['results'])
    assert read('neighbor_star_cut_layer_1_audit.json')['survivors'] == 6
    assert read('neighbor_star_cut_arcs_audit.json')['rejected'] == 5
    assert read('neighbor_star_cut_arcs_audit.json')['survivors'] == 1
    assert read('neighbor_arc_cuts.json')['direct_parent_exclusions'] == 0
    assert read('neighbor_arc_cut_certificate_audit.json')['verified_cuts'] == 5
    assert read('neighbor_star_cut_arcs_2_audit.json')['rejected'] == 1
    assert read('neighbor_arc_sat_audit.json')['cut_kinds'] == {'audited_initial':128,'neighbor_arc_failure':14,'empty_neighbor_domain':20}
    assert read('neighbor_arc_sat_audit.json')['direct_parent_exclusions'] == 0
    assert read('neighbor_arc_sat_layer_1_audit.json')['survivors'] == 6
    assert read('neighbor_arc_sat_arcs_audit.json')['survivors'] == 6
    assert read('arc_oracle_comparison.json')['domain_records'] == 45403
    assert read('choice_cut_domain_audit.json')['star_removals'] == 77
    assert read('choice_cut_arcs_audit.json')['survivors'] == 18
    assert read('choice_cut_frontier_seed.json')['status_counts'] == {'survivor':246,'rejected':0}
    assert read('choice_cut_forced_1_audit.json')['survivors'] == 235
    assert read('choice_cut_expanded_arcs_1_audit.json')['survivors'] == 205
    assert read('layered_choice_certificate_audit.json')['cut_length'] == 8
    assert read('layered_choice_certificate_audit.json')['direct_parent_exclusions'] == 0
    assert len(read('choice_cut_catalog_163.json')['cuts']) == 163
    assert read('choice_cut_catalog_163.json')['rejected_q023_models'] == [5]
    assert read('coarse_parent_language_audit.json')['extra_rejections'] == 40
    assert all(len(r) == 1 for r in read('coarse_parent_language.json')['child_roles'])
    assert read('coarse_refinement_audit.json')['survivor'] == 177
    assert read('coarse_refinement_audit.json')['coarse_rejection'] == 28
    assert read('choice_cut_pass_2_audit.json')['star_removals'] == 2
    assert read('choice_cut_forced_2_audit.json')['survivors'] == 170
    assert read('choice_cut_expanded_arcs_2_audit.json')['survivors'] == 130
    assert read('coarse_support_domain_audit.json')['incidences'] == 300497
    assert read('coarse_star_arc_audit.json')['remaining_extras'] == 160
    assert read('enlarged_sibling_roles.json')['all_sibling_roles_agree']
    assert read('enlarged_sibling_roles.json')['checked_incidences'] == 42658
    assert read('enlarged_sibling_probe_audit.json')['witnesses'] == 160
    assert read('enlarged_sibling_probe_audit.json')['additional_parent_exclusions'] == 0
    assert read('coarse_arc_frontier_1_audit.json')['survivor'] == 130
    assert read('coarse_star_arc_audit_2.json')['remaining_extras'] == 82
    assert read('coarse_arc_frontier_2_audit.json')['survivor'] == 82
    assert read('coarse_arc_frontier_2_audit.json')['coarse_rejection'] == 48
    receipt = dict(scope='Reproduction of finite research results, including counterexamples; objective remains open',
                   commands=records,input_hash_checks=checks,
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    filename = 'reproduction.json' if records else 'reproduction_hash_audit.json'
    (ROOT/'artifacts'/filename).write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'PASS: {len(records)} commands and {checks} input hashes; expected failures preserved.',flush=True)


if __name__ == '__main__':
    main()
