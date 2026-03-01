"""
Step 2 of dataset setup: Create the merged/ directory.

Flattens all scenarios from train/, val/, and test/ into a single merged/
directory using symbolic links.  Preprocessing scripts (preprocess.py) in
each data/Subset-A-*/ folder read from this merged/ directory so they can
look up any scenario by ID without knowing which split it belongs to.

Run this after link_test.py has created the test/ split.

Expected directory layout
-------------------------
<data_root>/
├── train/
├── val/
└── test/              ← created by link_test.py

After running this script
-------------------------
<data_root>/
└── merged/            ← one symlink per scenario pointing into train/, val/, or test/

Then create a symlink inside each relevant data/Subset-A-*/ folder:
    ln -s <data_root>/merged  <repo>/data/Subset-A-near/merged
    ln -s <data_root>/merged  <repo>/data/Subset-A-farA/merged
    (repeat for farB, farC)

Usage
-----
    python link_merged.py --data_root ~/datasets/OpenLane-V2
"""

import argparse
import os
from pathlib import Path


def create_merged(data_root: str) -> None:
    data_root = Path(data_root).expanduser().resolve()

    split_dirs = {
        'train': data_root / 'train',
        'val':   data_root / 'val',
        'test':  data_root / 'test',
    }
    merged_dir = data_root / 'merged'

    for name, split_dir in split_dirs.items():
        if not split_dir.exists():
            print(f'Error: {split_dir} does not exist. Run link_test.py first.')
            return

    merged_dir.mkdir(exist_ok=True)

    all_scenarios = []
    for split_name, split_dir in split_dirs.items():
        for d in sorted(split_dir.iterdir()):
            if d.is_dir():
                all_scenarios.append((split_name, d))

    print(f'Found {len(all_scenarios)} scenarios across all splits.')

    for split_name, scenario in all_scenarios:
        scenario_name = scenario.name
        target = merged_dir / scenario_name

        if target.exists() or target.is_symlink():
            print(f'  Already exists: {scenario_name}')
            continue

        rel_path = os.path.relpath(scenario, merged_dir)
        target.symlink_to(rel_path)
        print(f'  Linked {scenario_name} from {split_name}/')

    print('\nDone.')
    print(f'Create symlinks in your repo data/ folders, for example:')
    print(f'  ln -s {merged_dir}  <repo>/data/Subset-A-near/merged')
    print(f'  ln -s {merged_dir}  <repo>/data/Subset-A-farA/merged')
    print(f'  ln -s {merged_dir}  <repo>/data/Subset-A-farB/merged')
    print(f'  ln -s {merged_dir}  <repo>/data/Subset-A-farC/merged')
    print(f'Then run the corresponding preprocess.py scripts.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create merged/ directory unifying all train/, val/, test/ scenarios.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example:\n  python link_merged.py --data_root ~/datasets/OpenLane-V2',
    )
    parser.add_argument(
        '--data_root',
        type=str,
        required=True,
        help='Path to the root of your OpenLane-V2 dataset (contains train/, val/, test/).',
    )
    args = parser.parse_args()
    create_merged(args.data_root)
