# OLX.ba Testovi

## Problemi

- OLX koristi Cloudflare, tako da nekada može doći do problema sa pristupom stranici. Dodajemo umjetni delay izmedju testova, ali to nije zagarantovana solucija.
- OLX naizgledno nasumicno prikazuje cookie consent popup, cak i ako je vec prihvacen. Solucija je delay od 2 sekunde nakon log-in-a i dupli refresh stranice. (helpers/olx.py -> log_in)