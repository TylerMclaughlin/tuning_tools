library(data.table)
library(ggplot2)
#d <- data.table::fread('just_vs_edo_7_to_20.csv')
d <- data.table::fread('data/just_vs_edo_7_to_42.csv')


ggplot(d) + geom_line(aes(x = n_edo, y = cents_diff,color = root_1)) + facet_wrap(~pitch_class_smaller) + theme_classic()

ggplot(d) + geom_line(aes(x = n_edo, y = cents_diff,color = pitch_class_smaller)) + facet_wrap(~root_1) + theme_classic()

ggplot(d) + geom_raster(aes(x = root_1, y = pitch_class_smaller, fill = cents_diff)) + scale_fill_gradient(low="blue", high="red") + facet_wrap(~n_edo) + theme_bw()

d[, scaled.cents.diff := scale(cents_diff), by = n_edo]

ggplot(d) + geom_histogram(aes(x = cents_diff, fill = factor(n_edo) ), bins = 100) + scale_fill_discrete()

ggplot(d) + geom_histogram(aes(x = cents_diff, fill = factor(matched_pitch_class) ), bins = 100) + scale_fill_discrete()


ggplot(d) + geom_raster(aes(x = root_1, y = pitch_class_smaller, fill = scaled.cents.diff)) +
      scale_fill_gradient(name = 'deviation in cents', low="blue", high="red") + facet_wrap(~n_edo) + theme_bw() +
      xlab('just diatonic root') + ylab('just diatonic pitch class')

d[,just_pitch_class := paste0(pitch_class_smaller,"_just"), .()]

wide.data <- dcast(d, n_edo ~ just_pitch_class +  root_1, value.var = 'scaled.cents.diff')
dim(wide.data)
# 36 50.  36 edos, 7x7 = 49 features, 1 edo name (label)
pca <- prcomp(wide.data[,c(2:50)])

pca.dt <- data.table(pca$x)
pca.dt[, n_edo := wide.data$n_edo]

# scree plot, proportion of variance explained by eigenvector
pc.variance <- (pca$sdev)^2
proportion.variance.explained <- pc.variance / sum(pc.variance)
plot(proportion.variance.explained)
# first 9 principal components are useful.

library(ggrepel)
# PC1 vs PC2
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(n_edo))) + geom_text_repel(aes(label = factor(n_edo)))
ggplot(pca.dt, aes(x = PC2, y = PC3)) + geom_point(aes( color = factor(n_edo))) + geom_text_repel(aes(label = factor(n_edo)))

# DIRICHLET PROCESS CLUSTERING
library(dirichletprocess)
dp <- DirichletProcessMvnormal(as.matrix(wide.data[,c(2:50)]))
dp <- Fit(dp, 1000, progressBar=TRUE)
dp$clusterLabels
# all 1s.  hmmm

dp <- DirichletProcessMvnormal(as.matrix(pca.dt[,c(1:9)]) )
dp <- Fit(dp, 1000, progressBar=TRUE)
dp$clusterLabels
pca.dt$dp.cluster.label <- dp$clusterLabels
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(dp.cluster.label))) + geom_text_repel(aes(label = factor(n_edo)))

# KMEANS CLUSTERING
set.seed(20)
kmeans.clusters <- kmeans(wide.data[,c(2:50)], 5)
pca.dt$kmeans.cluster <- kmeans.clusters$cluster
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(kmeans.cluster))) + geom_text_repel(aes(label = factor(n_edo)))

kmeans.clusters <- kmeans(pca.dt[,c(1:9)], 5)
pca.dt$kmeans.cluster <- kmeans.clusters$cluster
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(kmeans.cluster))) + geom_text_repel(aes(label = factor(n_edo)))


# UMAP
library(umap)
edo.umap = umap(wide.data[,c(2:50)])
umap.dt = data.table(edo.umap$layout)
umap.dt[, n_edo := wide.data$n_edo]
ggplot(umap.dt, aes(x = V1, y = V2)) + geom_point(aes( color = factor(n_edo))) + geom_text_repel(aes(label = factor(n_edo)))



# look at correlation between matrices.
data.matrix <- as.matrix(wide.data[,c(2:50)])
rownames(data.matrix) <- wide.data$n_edo
cor.matrix <- cor(t(data.matrix))
melted.cor.matrix <- melt(cor.matrix)
ggplot(melted.cor.matrix, aes(x=Var1, y=Var2, fill=value)) + geom_tile() + scale_fill_gradient(name = 'correlation', low="violet", high="green")

library(ComplexHeatmap)
Heatmap(cor.matrix)

distance <- dist(data.no.labels)
plot(distance)
