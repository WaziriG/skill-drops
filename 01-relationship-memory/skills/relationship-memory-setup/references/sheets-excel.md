# Store notes: Excel and Google Sheets

Column names and meanings are in `schema.md`. This file covers the spreadsheet routes.

## Excel (the most automated route)

`inbox_enrich.py --apply` writes straight into the workbook. Nothing else is needed.

- The spine lives on a sheet named **People** (or pass `--sheet`), formatted as an Excel table, headers in row 1.
- The run adds any missing history columns at the right, writes Warmth and Follow-up Status as live formulas (they recalculate every day you open the file), and keeps a **Discoveries** sheet. Type `yes` or `x` in its Promote column, then run `--promote`.
- A dated copy goes to `_archive/` next to the workbook before every write.
- Next Step is yours: the run never writes it. Open Loops only grows, one dated line per new loop. A Follow-up Cadence you typed is never replaced.
- **Close the workbook before a run.** The script cannot write to a file Excel has open, and a synced copy (OneDrive, Dropbox) can conflict if it is open on another machine.
- Keep the People workbook plain: no charts, pivot tables or images in the same file. The library that writes it (openpyxl) can drop them. Build dashboards in a separate workbook that reads this one.
- Start from `mock/People.xlsx` in the kit if you do not have a workbook yet.

Formulas, if you add the columns by hand (structured references, table named People):

**Warmth**
```
=IF(N([@[Emails Exchanged]])=0,0,ROUND(MIN(40,[@[Emails Exchanged]]*4)+IF([@[Last Email]]="",0,MAX(0,40-(TODAY()-[@[Last Email]])/9))+IF([@[Last Email From]]="Them",20,0),0))
```

**Warm Enough to Ask**
```
=IF([@Warmth]>=35,"Yes","No")
```

**Follow-up Status**
```
=IF([@[Last Email]]="","No email history",IF(AND([@[Last Email From]]="Them",TODAY()-[@[Last Email]]<=60,[@[Know Them?]]<>"No"),"Reply owed",IF(TODAY()-[@[Last Email]]>3*[@[Follow-up Cadence]],"Dormant",IF([@[Last Email]]+[@[Follow-up Cadence]]<TODAY(),"Overdue",IF([@[Last Email]]+[@[Follow-up Cadence]]-TODAY()<=14,"Due soon","On track")))))
```

Useful filters: Know Them? = Yes, sorted by Warmth (largest first), is your "Warmest first" view.

## CSV

Same as Excel, without formulas: `--apply` writes computed Warmth and Follow-up Status values (they are correct on the day of the run), and new people go to `<file>-discoveries.csv`.

## Google Sheets (least automated; be honest with the owner about this)

The script cannot write to Google Sheets directly. Two options:

1. **With a Google Sheets connector in Claude Code**: export the People tab as JSON (with the row number as `id`), run `inbox_enrich.py --out changes.json`, and have Claude write each `fields` value into its row. Keep the formulas in the sheet.
2. **Without a connector**: File → Download → Microsoft Excel (.xlsx), run the Excel route with `--apply`, then File → Import → Upload → "Replace current sheet". Fine weekly; tedious daily.

Google Sheets formulas (row 2 shown; headers as in `schema.md`; adjust the column letters to your sheet):
```
Warmth:            =IF(N(K2)=0,0,ROUND(MIN(40,K2*4)+IF(N2="",0,MAX(0,40-(TODAY()-N2)/9))+IF(O2="Them",20,0),0))
Follow-up Status:  =IF(N2="","No email history",IF(AND(O2="Them",TODAY()-N2<=60,G2<>"No"),"Reply owed",IF(TODAY()-N2>3*S2,"Dormant",IF(N2+S2<TODAY(),"Overdue",IF(N2+S2-TODAY()<=14,"Due soon","On track")))))
```
(K = Emails Exchanged, N = Last Email, O = Last Email From, G = Know Them?, S = Follow-up Cadence in the kit's column order.)
