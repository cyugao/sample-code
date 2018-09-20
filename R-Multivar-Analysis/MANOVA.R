
onewaymanova <- function(A, B) {
  d <- dim(A)
  g <- d[1]
  b <- d[2]
  Atotalmean <- mean(A)
  Arowmean <- rowMeans(A)
  Acolmean <- colMeans(A)
  Amean <- matrix(rep.int(Atotalmean, g*b), nrow = 3)
  Afac1 <- outer(Arowmean, rep.int(1, b)) - Amean
  Afac2 <- outer(rep.int(1, g), Acolmean) - Amean
  Ares <- A - Afac1 - Afac2 - Amean
  cat("A:\n")
  cat("mean:\n")
  print(Amean)
  cat("fac1:\n")
  print(Afac1)
  cat("fac2:\n")
  print(Afac2)
  cat("res:\n")
  print(Ares)
  Btotalmean <- mean(B)
  Browmean <- rowMeans(B)
  Bcolmean <- colMeans(B)
  Bmean <- matrix(rep.int(Btotalmean, g*b), nrow = 3)
  Bfac1 <- outer(Browmean, rep.int(1, b)) - Bmean
  Bfac2 <- outer(rep.int(1, g), Bcolmean) - Bmean
  Bres <- B - Bfac1 - Bfac2 - Bmean
  cat("B:\n")
  cat("mean:\n")
  print(Bmean)
  cat("fac1:\n")
  print(Bfac1)
  cat("fac2:\n")
  print(Bfac2)
  cat("res:\n")
  print(Bres)
  obsroll <- rbind(c(A), c(B))
  SSobs <- obsroll %*% t(obsroll)
  print(SSobs)
  meanroll <- rbind(c(Amean), c(Bmean))
  SSmean <- meanroll %*% t(meanroll)
  print(SSmean)
  fac1roll <- rbind(c(Afac1), c(Bfac1))
  SSfac1 <- fac1roll %*% t(fac1roll)
  print(SSfac1)
  fac2roll <- rbind(c(Afac2), c(Bfac2))
  SSfac2 <- fac2roll %*% t(fac2roll)
  print(SSfac2)
  resroll <- rbind(c(Ares), c(Bres))
  SSres <- resroll %*% t(resroll)
  print(SSres)
  SScorrected <- SSobs - SSmean
  print(SScorrected)
}

