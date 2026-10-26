#!/usr/bin/env python3
"""savings.py — what freeing up a full drive is worth, in dollars, with every assumption shown.

Every price is an input. The defaults are typical US prices; check current ones before quoting a number.

  python3 savings.py --freed-gb 64 --disk-gb 500 --tier-step-cost 400 --hours-saved-per-week 1 --hourly-value 75
"""
import argparse

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument("--freed-gb", type=float, required=True, help="GB moved off the computer")
p.add_argument("--disk-gb", type=float, default=0, help="internal disk size, for the percentage line")
p.add_argument("--internal-per-gb", type=float, default=0.40,
               help="what the computer maker charges per extra GB of internal storage (default 0.40: about $200 per 512 GB step)")
p.add_argument("--drive-per-gb", type=float, default=0.03, help="external hard drive cost per GB (default 0.03: about $120 for 4 TB)")
p.add_argument("--copies", type=int, default=2, help="how many drive copies you keep (default 2)")
p.add_argument("--drives-already-owned", action="store_true", help="drives were sitting in a drawer: copy cost is $0")
p.add_argument("--cloud-monthly", type=float, default=9.99, help="the cloud plan you would otherwise pay for (default 9.99: 2 TB tier)")
p.add_argument("--years", type=float, default=3, help="years to count recurring costs over (default 3)")
p.add_argument("--tier-step-cost", type=float, default=0,
               help="price of the next storage tier you no longer need on your NEXT computer (e.g. 400 for 1 TB -> 2 TB)")
p.add_argument("--computer-price", type=float, default=0, help="price of a replacement computer, if freeing space delays buying one")
p.add_argument("--life-years", type=float, default=5, help="useful life of that computer (default 5)")
p.add_argument("--months-delayed", type=float, default=0, help="months the replacement is pushed back")
p.add_argument("--hours-saved-per-week", type=float, default=0, help="time no longer lost to cleanup, crashes, 'disk full' errors")
p.add_argument("--hourly-value", type=float, default=0, help="what an hour of your time is worth")
a = p.parse_args()

copy_cost = 0 if a.drives_already_owned else a.freed_gb * a.drive_per_gb * a.copies
lines = []

internal_equiv = a.freed_gb * a.internal_per_gb
lines.append(("Same space bought as internal storage", internal_equiv,
              f"{a.freed_gb:.0f} GB x ${a.internal_per_gb:.2f}/GB"))
cloud = a.cloud_monthly * 12 * a.years
lines.append((f"Cloud plan you skip ({a.years:.0f} yr)", cloud, f"${a.cloud_monthly:.2f}/mo x {12 * a.years:.0f} months"))
if a.tier_step_cost:
    lines.append(("Smaller storage tier on the next computer", a.tier_step_cost, "one-time, at purchase"))
if a.computer_price and a.months_delayed:
    delay = a.computer_price / (a.life_years * 12) * a.months_delayed
    lines.append(("Replacement pushed back", delay,
                  f"${a.computer_price:,.0f} / {a.life_years:.0f} yr life x {a.months_delayed:.0f} months"))
if a.hours_saved_per_week and a.hourly_value:
    time_value = a.hours_saved_per_week * a.hourly_value * 48 * a.years
    lines.append((f"Time back ({a.years:.0f} yr)", time_value,
                  f"{a.hours_saved_per_week:g} h/week x ${a.hourly_value:.0f}/h x 48 weeks x {a.years:.0f}"))

print("| What it replaces | Value | How it's figured |\n|---|---:|---|")
for name, value, how in lines:
    print(f"| {name} | ${value:,.0f} | {how} |")
print(f"| **Cost of two drive copies** | **-${copy_cost:,.0f}** | "
      f"{'drives already owned' if a.drives_already_owned else f'{a.freed_gb:.0f} GB x ${a.drive_per_gb:.2f}/GB x {a.copies}'} |")

# Cloud and internal storage are alternatives to each other, so count only the larger one.
alternatives = max(internal_equiv, cloud)
extras = sum(v for n, v, _ in lines[2:])
net = alternatives + extras - copy_cost
print(f"\n**Net value: about ${net:,.0f}** "
      f"(the larger of internal-storage or cloud, plus the other lines, minus drive cost).")
if a.disk_gb:
    print(f"Space freed: {a.freed_gb:.0f} GB = {100 * a.freed_gb / a.disk_gb:.0f}% of a {a.disk_gb:.0f} GB disk.")
print(f"Per GB: two drive copies cost ${a.drive_per_gb * a.copies:.2f}/GB vs ${a.internal_per_gb:.2f}/GB built in "
      f"— about {a.internal_per_gb / (a.drive_per_gb * a.copies):.0f}x cheaper.")
