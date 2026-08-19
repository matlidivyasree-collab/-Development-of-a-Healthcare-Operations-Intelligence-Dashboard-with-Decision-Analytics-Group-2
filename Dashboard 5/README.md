# Medical Operations Intelligence — Dashboard 5

**Health Programs & Population Vulnerability**

A Streamlit dashboard that measures public health programme
performance and identifies the populations that need attention most.

---

## Folder structure

```
Dashboard 2/
├── .streamlit/
│   └── config.toml              theme colours for Streamlit itself
├── dashboards/
│   └── 4_Health_Programs_Population_Vulnerability.py
├── data/
│   ├── fact_health_programs.csv
│   ├── dim_program.csv
│   ├── dim_state.csv
│   ├── dim_date.csv
│   └── dim_source.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py           cached CSV loading + star-schema joins
│   ├── filters.py               shared sidebar filter panel
│   ├── kpis.py                  KPI calculation and formatting
│   └── styling.py               shared CSS + reusable UI components
├── app.py                       entry point, chooses the dashboard
├── README.md
└── requirements.txt
```

Each part has one job. `app.py` sets the page up and builds the
navigation; every chart and calculation lives in `dashboards/` and
`src/`.

Page files are named `N_Title_Words.py`. The leading number sets the
order in the sidebar and is stripped from the label, so
`4_Health_Programs_Population_Vulnerability.py` appears as
*Health Programs Population Vulnerability*. Numbering starts at 0,
so Dashboard 5 is file `4_`.

A new dashboard is added by dropping its file into `dashboards/`.
Nothing in `app.py` needs to change.

---

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

Run the command from the project folder, so that `src` and
`dashboards` can be imported.

---

## Data model

A star schema of one fact table and four dimensions. 6,981 raw fact
rows covering 32 states, 6 programmes and 36 months.

| Table | Rows | Grain | Joins on |
|---|---|---|---|
| `fact_health_programs` | 6,981 | one row per state, month and programme | — |
| `dim_program` | 6 | one row per programme | `program_id` |
| `dim_state` | 32 | one row per state | `state_id` |
| `dim_date` | 36 | one row per month | `date_id` |
| `dim_source` | 6 | one row per source | not joined — see limitations |

After cleaning, 6,885 rows remain.

---

## Key performance indicators

| KPI | Calculation |
|---|---|
| Program Coverage | average of `program_coverage_pct` |
| People Screened | sum of `people_screened` |
| Beneficiaries Reached | sum of `beneficiaries_reached` |
| Maternal Health Beneficiaries | sum of `maternal_health_beneficiaries` |
| Child Immunization | sum of `child_immunization_count` |
| High-Risk Individuals | sum of `high_risk_individuals` |
| Chronic Disease Patients | sum of `chronic_disease_patients` |
| Health Vulnerability Index | average of `health_vulnerability_index` |

Large counts are shown in short form — `K` thousand, `M` million,
`B` billion — because a figure such as 10,347,642,180 does not fit
inside a card and was being cut off. The exact figure is printed in
small text under each value and also appears on hover, so nothing is
hidden from the reader.

---

## Visuals

1. **Program Coverage Over Time** — line chart, one line per year,
   months in calendar order.
2. **People Screened vs Beneficiaries Reached** — grouped bars by
   state.
3. **Population Distribution by State** — stacked bars of children,
   adults and elderly.
4. **High-Risk Population by State** — treemap.
5. **Composite Health Vulnerability Index** — bar chart by state.
6. **Socioeconomic Score vs Health Vulnerability** — bubble chart,
   one point per state, with the correlation printed underneath.

---

## Data quality decisions

Every decision below is applied before any figure is calculated, and
the counts are reported in a note at the top of the dashboard.

- **Duplicate fact rows** are dropped. The raw file contains exact
  duplicates that would inflate every total.
- **Dimension tables are de-duplicated on their id** before the
  merge. A repeated id would fan out the fact table and make every
  total too high.
- **Negative counts are removed.** A negative number of high-risk
  individuals is not possible.
- **Text and blank values in number columns** become `NaN` rather
  than breaking a chart.
- **Population columns use the average, not the sum.** Children,
  adults and elderly are the only columns that are constant within
  a state and month; they are repeated on all six programme rows.
  They are read from a de-duplicated frame so the population is not
  multiplied by the number of programmes. Every other measure,
  including the immunisation count, genuinely varies by programme
  and is summed from the filtered rows.

---

## Known limitations

- **Visual 5 is a bar chart, not a filled map.** The filled map
  needs an India GeoJSON boundary file, which is not part of this
  dataset.
- **No Primary Source filter.** `dim_source.csv` is supplied, but
  the fact table has no `source_id`, so there is no key to join on
  and the dimension cannot be filtered against.
- **Child Immunization is implausibly large in the source data.**
  A single state-month-programme row records around 8–12 million
  immunisations against a child population of about 13 million.
  The aggregation is correct, but the underlying column looks
  either cumulative or mis-scaled, so the total should be checked
  before it is quoted.

---

## Filters

State, Year, Month and Programme, all in the sidebar and all
applying to every KPI and every chart. `All` means no filter is
applied for that box. If a combination returns no rows, the
dashboard says so instead of drawing empty charts.
