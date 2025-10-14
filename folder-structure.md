# Suggestion 1

- clear difference between data and documentation
- deeper hierarchy

```
.
├── data
│    ├── input
│    │    ├── daschland-data-model
│    │    ├── multimedia
│    │    ├── nodegoat
│    │    ├── spreadsheets
│    │    └── xml
│    └── output
│        ├── daschland.json
│        └── data_daschland.xml
├── documentation
│    └── Project Documentation.docx
├── pyproject.toml
├── README.md
├── src
└── test
    └── testdata
```


# Suggestion 2

- focus on input / output of data
- documentation is clearly separate
- flatter hierarchy

```
.
├── documentation
│    └── Project Documentation.docx
├── input
│    ├── daschland-data-model
│    ├── multimedia
│    ├── nodegoat
│    ├── spreadsheets
│    └── xml
├── output
│    ├── daschland.json
│    └── data_daschland.xml
├── pyproject.toml
├── README.md
├── src
└── test
    └── testdata
```


# Suggestion 3

- focus on files, a bit of a catch all
- content is a mix only output is clearly separated from files that are used as input (implicit)
- documentation is also in files

```
.
├── files
│    ├── daschland-data-model
│    ├── documentation
│    │    └── Project Documentation.docx
│    ├── multimedia
│    ├── nodegoat
│    ├── output
│    │    ├── daschland.json
│    │    └── data_daschland.xml
│    ├── spreadsheets
│    └── xml
├── pyproject.toml
├── README.md
├── src
└── test
    └── testdata
```

