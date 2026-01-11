-  Question 1:
Show the highest price of each product on each date. All fields should be kept in the result table.
```python
data = {
    "date": ["2023-04-01", "2023-04-01", "2023-04-01", "2023-04-02", "2023-04-02", "2023-04-03", "2023-04-03"],
    "product": ["Apple", "Banana", "Apple", "Banana", "Banana", "Apple", "Banana"],
    "sales": [100, 200, 150, 100, 150, 200, 180]
}

df = pd.DataFrame(data)
df
```

Ans:
```python
df_sorted = df.sort_values(
    ["date", "sales"],
    ascending=[True, False],
)

df_sorted["row_number"] = df_sorted.groupby(["date", "product"]).cumcount() + 1

df_sorted[
    df_sorted["row_number"] == 1
][
    ["date", "product", "sales"]
]
```
