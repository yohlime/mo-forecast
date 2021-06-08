*write('fcst_verify12hr.csv', 'date, model, RMSE, MB ,scorr, sd')
*write('fcst_verify24hr.csv', 'date, model, RMSE, MB ,scorr, sd')
*write('fcst_verify48hr.csv', 'date, model, RMSE, MB ,scorr, sd')
write('fcst_verify.csv', 'fcst_hrs, date, model, RMSE, MB ,scorr, sd')
quit

