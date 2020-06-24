.. _release-v13-0-qserv-dax:

##########################################
Fall 2016 QServ and Data Access Highlights
##########################################

- Query analysis fixes (more robust handling of ORDER BY, fix for missed usages of chunk/subchunk secondary index to limit query dispatch to involved chunks).

- Shared scan improvements (fixes for "snail scan" long-running outlier query scan, scan table memory locking fixes/improvements).

- Many containerization improvements (container sizes reduced by removing mariadb unit tests and intermediate compilation products, container-host timezone sync, more robust build and deploy scripts).

- Database connection management fixes for wmgr service to enable parallelized usage of qserv loader script.

- XRootD now logs via the LSST log package.
