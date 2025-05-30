# Pyrite

## Adding New Tables to Pyrite Reports

### 1. Register Test IDs
In `./types.py`, add the ID(s) for your test(s).

**If adding new tests:**
- Add a test description in `./reports/appendix_a.py`
- Add introduction details in `./reports/introduction.py`

### 2. Create the Table File
In `./tables/`, create a new Python file for your table. Use an existing similar table as a template.

**Required Components:**

**DataProducer Class**
- Inherits from `base.DataProducer`
- Implements `fetch()` method that returns `tuple[tuple[str, ...], ...]`
  - Each inner tuple represents a table row
  - Each string represents a cell's content
- Includes `test_ids` class method containing associated test IDs from `types.py`

**TableSection Class**
- Inherits from both `base.WordTableSectionAddToMixin` and `base.WordTableSection`
- Defines two required attributes:
  - `data_source`: Your DataProducer instance
  - `formatters`: Table formatting configuration (see other tables or docstrings for options)

### 3. Register the Table
In `./reports/reports.py`:
1. Add your table to the `_PyriteTableCollection` class
2. Add the table section to the desired report version(s) (currently only Alabaster exists)
