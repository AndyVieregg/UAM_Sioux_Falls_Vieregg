library(DBI)

con <- dbConnect(RPostgres::Postgres(),
                 dbname= 'matsim',
                 host = 'localhost',
                 port = 5433,
                 user = 'postgres',
                 password = 'hainich',
                 options="-c search_path=uam_bl")

dbWriteTable (con, 'linkstats', linkstatsu, overwrite=TRUE)
