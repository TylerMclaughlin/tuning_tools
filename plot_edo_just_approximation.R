library(data.table)
library(ggplot2)
#d <- data.table::fread('just_vs_edo_7_to_20.csv')
d <- data.table::fread('data/just_vs_edo_7_to_42.csv')


ggplot(d) + geom_line(aes(x = n_edo, y = cents_diff,color = root_1)) + facet_wrap(~pitch_class_smaller) + theme_classic()

ggplot(d) + geom_line(aes(x = n_edo, y = cents_diff,color = pitch_class_smaller)) + facet_wrap(~root_1) + theme_classic()

ggplot(d) + geom_raster(aes(x = root_1, y = pitch_class_smaller, fill = cents_diff)) + scale_fill_gradient(low="blue", high="red") + facet_wrap(~n_edo) + theme_bw()

d[, scaled.cents.diff := scale(cents_diff), by = n_edo]

ggplot(d) + geom_raster(aes(x = root_1, y = pitch_class_smaller, fill = scaled.cents.diff)) +
      scale_fill_gradient(name = 'deviation in cents', low="blue", high="red") + facet_wrap(~n_edo) + theme_bw() +
      xlab('just diatonic root') + ylab('just diatonic pitch class')

