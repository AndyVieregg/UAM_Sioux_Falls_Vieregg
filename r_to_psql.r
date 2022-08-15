library(DBI)

con <- dbConnect(RPostgres::Postgres(),
                 dbname= 'matsim',
                 host = 'localhost',
                 port = 5433,
                 user = 'postgres',
                 password = 'hainich',
                 options="-c search_path=uam_sp_ap")

dbWriteTable (con, 'linkstats', linkstatsap, overwrite=TRUE)

