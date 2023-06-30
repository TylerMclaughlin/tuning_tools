library(data.table)
library(ggplot2)
#d <- data.table::fread('just_vs_edo_7_to_20.csv')
#d <- data.table::fread('data/just_vs_edo_7_to_42.csv')
#d <- data.table::fread('data/just_vs_edo_7_to_106.csv')
d <- data.table::fread('data/just_vs_edo_7_to_406.csv')

# show deviation

d_mean = d[,.(mean_cents_diff = mean(cents_diff)), .(n_edo)]

ggplot(d_mean[n_edo <=  42]) + geom_line(aes(x = n_edo, y = mean_cents_diff)) +  theme_classic()

#  figure 1:  mean deviation approaches zero.
d_mean = d[root_1 == 'C',.(mean_cents_diff = mean(cents_diff)), .(n_edo)]
ggplot(d_mean[n_edo <=  100]) + geom_line(aes(x = n_edo, y = mean_cents_diff)) +  theme_classic() + xlim(7,100)

d_mean = d[root_1 == 'E',.(mean_cents_diff = mean(cents_diff)), .(n_edo)]
ggplot(d_mean[n_edo <=  100]) + geom_line(aes(x = n_edo, y = mean_cents_diff)) +  theme_classic() + xlim(7,100)

ggplot(d[n_edo <=  42]) + geom_line(aes(x = n_edo, y = cents_diff,color = root_1)) + facet_wrap(~pitch_class_smaller) + theme_classic()

ggplot(d) + geom_line(aes(x = n_edo, y = cents_diff,color = pitch_class_smaller)) + facet_wrap(~root_1) + theme_classic()

ggplot(d[n_edo <= 42]) + geom_raster(aes(x = root_1, y = pitch_class_smaller, fill = cents_diff)) + scale_fill_gradient(low="blue", high="red") + facet_wrap(~n_edo) + theme_bw()

# mean absolute cents diff
ggplot(d[,.(mean(abs(cents_diff))), by=list(n_edo)]) + geom_line(aes(x = n_edo, y = V1))
# maximum absolute cents diff
ggplot(d[,.(max(abs(cents_diff))), by=list(n_edo)]) + geom_line(aes(x = n_edo, y = V1)) + 
        geom_hline(yintercept = 3.3) + ylab('Maximum Absolute Deviation from Just Interval (cents)') + xlab('N equal divisions per octave (EDO)')
#:)


d[, scaled.cents.diff := scale(cents_diff), by = n_edo]

ggplot(d) + geom_histogram(aes(x = cents_diff, fill = factor(n_edo) ), bins = 100) + scale_fill_discrete()

ggplot(d) + geom_histogram(aes(x = cents_diff, fill = factor(matched_pitch_class) ), bins = 100) + scale_fill_discrete()

# main MAJI plot
ggplot(d[n_edo %in% db.cluster.1]) + geom_raster(aes(x = root_1, y = pitch_class_smaller, fill = scaled.cents.diff)) +
      scale_fill_gradient(name = 'deviation in cents', low="blue", high="red") + facet_wrap(~n_edo) + theme_bw() +
      xlab('just diatonic root') + ylab('just diatonic pitch class')

# 2 blobs
db.cluster.15 <- c(36,  55, 108, 161)# 207)
db.cluster.4 <- c(10,  56,  63, 109, 116)

#4 blobs
db.cluster.10 <- c(17, 51, 104, 169)
db.cluster.7 <- c(14, 67, 101, 120)

db.cluster.6 <- c(13, 20, 32, 54)
db.cluster.5 <- c(11, 21, 33, 40)


# pearls
db.cluster.12 <- c(25, 37, 44, 59, 78)
db.cluster.3 <- c(9, 28, 62, 74, 81)

db.cluster.2 <- c(8, 42, 49, 61, 73)
db.cluster.16 <- c(45, 57, 76, 110)

db.cluster.0 <- c(220, 273, 299, 338, 391)
db.cluster.17 <- c(103, 156, 168, 221)

db.cluster.2 <- c(8, 42, 49, 61, 73)
db.cluster.16 <- c(45, 57, 76, 110)

# crescents
db.cluster.13 <- c(26, 48, 79, 91, 132)
db.cluster.14 <- c(27, 39, 70, 92, 145)

# ring
db.cluster.1 <- c(7, 12, 19, 22, 24, 29, 31, 34, 41,
                  46, 53, 58, 65, 72, 77,
                  82, 84, 87, 89, 94, 96, 99) #38, 43, 50, 60


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

library(plotly)
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC3, color = ~n_edo)
plot_ly(data = pca.dt, x = ~PC4, y = ~PC5, z = ~PC6, color = ~n_edo)

plotly_colors = 

# DIRICHLET PROCESS CLUSTERING
library(dirichletprocess)
dp <- DirichletProcessMvnormal(as.matrix(wide.data[,c(2:50)]))
dp <- Fit(dp, 1000, progressBar=TRUE)
dp$clusterLabels
# all 1s.  hmmm

#dp <- DirichletProcessMvnormal(as.matrix(pca.dt[,c(1:9)]) )
dp <- DirichletProcessMvnormal(as.matrix(pca.dt[,c(1:11)]) )
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
set.seed(36)
edo.umap = umap(wide.data[,c(2:50)], n_components = 2)
umap.dt = data.table(edo.umap$layout)
umap.dt[, n_edo := wide.data$n_edo]
ggplot(umap.dt, aes(x = V1, y = V2)) + geom_point(aes( color = factor(n_edo))) + geom_text_repel(aes(label = factor(n_edo))) + theme(legend.position = "none")
ggplot(umap.dt, aes(x = V1, y = V2)) + geom_point(aes( color = n_edo)) +  theme(legend.position = "none") + scale_color_viridis_c()
edo.umap = umap(wide.data[,c(2:50)], n_components = 3)
umap.dt = data.table(edo.umap$layout)
umap.dt[, n_edo := wide.data$n_edo]
ggplot(umap.dt, aes(x = V2, y = V3)) + geom_point(aes( color = n_edo)) +  theme(legend.position = "none") + scale_color_viridis_c()
plot_ly(data = umap.dt[c(1:100)], x = ~V1, y = ~V2, z = ~V3, color = ~n_edo)
plot_ly(data = umap.dt[c(100:200)], x = ~V1, y = ~V2, z = ~V3, color = ~n_edo)
plot_ly(data = umap.dt, x = ~V1, y = ~V2, z = ~V3, color = ~n_edo)
# aabout 14 clusters.
kmeans.clusters <- kmeans(wide.data[,c(2:50)], 14)
pca.dt$kmeans.cluster <- kmeans.clusters$cluster
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(kmeans.cluster)))

kmeans.clusters <- kmeans(pca.dt[,c(1:11)], 14)
pca.dt$kmeans.cluster <- kmeans.clusters$cluster
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(kmeans.cluster))) 

# definitely calls for dbscan
# DBSCAN
library(dbscan)
dbscan.clusters <- dbscan(pca.dt[,c(1:9)], eps = 5)
table(dbscan.clusters$cluster)
# 14 total clusters
pca.dt$dbscan.cluster <- dbscan.clusters$cluster
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(dbscan.cluster))) 
ggplot(pca.dt, aes(x = PC1, y = PC2)) + geom_point(aes( color = factor(dbscan.cluster)))# + scale_color_manual(RColorBrewer::brewer.pal(12, "Set3"))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC3, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC4, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC5, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC6, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC7, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC8, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC2, z = ~PC11, color = ~factor(dbscan.cluster))

plot_ly(data = pca.dt, x = ~PC2, y = ~PC3, z = ~PC4, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC1, y = ~PC4, z = ~PC5, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt, x = ~PC5, y = ~PC6, z = ~PC7, color = ~factor(dbscan.cluster))

plot_ly(data = pca.dt, x = ~PC3, y = ~PC5, z = ~PC8, color = ~factor(dbscan.cluster))

# color by n_edo
plot_ly(data = pca.dt[c(1:100)], x = ~PC1, y = ~PC2, z = ~PC3, color = ~factor(n_edo))
plot_ly(data = pca.dt[c(1:100)], x = ~PC4, y = ~PC5, z = ~PC6, color = ~factor(dbscan.cluster))

plot_ly(data = pca.dt[c(1:100)][dbscan.cluster == 1][!n_edo %in% c(43,38,50,60)], x = ~PC4, y = ~PC5, z = ~PC6, color = ~PC2)

# 2D
plot_ly(data = pca.dt, x = ~PC3, y = ~PC5, color = ~factor(dbscan.cluster))
plot_ly(data = pca.dt[dbscan.cluster == 1], x = ~PC3, y = ~PC5, color = ~factor(dbscan.cluster))
# clearly shows that 43, 50, 38, 60, etc are not on circle

library(GGally)
p <- ggpairs(data = pca.dt[,c(1:9)], ggplot2::aes(colour=factor(pca.dt$dbscan.cluster)))

for(i in 1:p$nrow) {
  for(j in 1:p$ncol){
    p[i,j] <- p[i,j] + 
      scale_color_manual(values=c("red", "blue", "green", "yellow", "black"))  
  }
}

p

# 

# plot cluster jumping:
plot(dbscan.clusters$cluster,type = 'line')

# UMAP DBSCAN
dbscan.umap = umap(wide.data[,c(2:50)], n_components = 3)
umap.dt = data.table(dbscan.umap$layout)
umap.dt[, dbscan.cluster := pca.dt$dbscan.cluster]
#saveRDS(umap.dt, file = 'umap.dt.16.dbscan.clusters.1.rds')
plot_ly(data = umap.dt[c(1:42)], x = ~V1, y = ~V2, z = ~V3, color = ~factor(dbscan.cluster))
plot_ly(data = umap.dt[c(43:84)], x = ~V1, y = ~V2, z = ~V3, color = ~factor(dbscan.cluster))
plot_ly(data = umap.dt, x = ~V1, y = ~V2, z = ~V3, color = ~factor(dbscan.cluster))


# look at correlation between matrices.
data.matrix <- as.matrix(wide.data[,c(2:50)])
data.matrix <- as.matrix(pca.dt[,c(1:9)])
rownames(data.matrix) <- wide.data$n_edo
cor.matrix <- cor(t(data.matrix))
melted.cor.matrix <- melt(cor.matrix)
ggplot(melted.cor.matrix, aes(x=Var1, y=Var2, fill=value)) + geom_tile() + scale_fill_gradient(name = 'correlation', low="violet", high="green")

library(ComplexHeatmap)
f2 = circlize::colorRamp2(seq(min(-1), max(1), length = 3), c("blue", "#EEEEEE", "red"), space = "RGB")
Heatmap(cor.matrix, col = f2)


# DISTANCE MATRIX
distance.matrix <- dist(wide.data[,c(2:50)])
hist(c(distance.matrix))
hist(c(distance.matrix), breaks = 1000)
#distance <- dist(data.no.labels)
#plot(distance)


distance.matrix.1 <- dist(wide.data[c(1:100),c(2:50)])
hist(c(distance.matrix.1), breaks = 300)

distance.matrix.2 <- dist(wide.data[c(100:200),c(2:50)])
hist(c(distance.matrix.2), breaks = 300)

distance.matrix.3 <- dist(wide.data[c(200:300),c(2:50)])
hist(c(distance.matrix.3), breaks = 300)

distance.matrix.4 <- dist(wide.data[c(300:400),c(2:50)])
hist(c(distance.matrix.4), breaks = 300)

# DISTANCE MATRIX ON PRINCIPAL COMPONENTS
distance.matrix <- dist(pca.dt[, c(1:9)])
hist(distance.matrix, breaks = 1000)


# PCA ON RING CLUSTER ONLY

ring.pca.dt <- pca.dt[dbscan.cluster == 1][!n_edo %in% c(43, 38, 50, 60)][c(1:89), c(1:50)]

# don't use the edo labels for PCA
ring.pc <- prcomp(ring.pca.dt[,c(1:49)])
ring.pc.dt <- data.table(ring.pc$x)
ring.pc.dt$n_edo <- ring.pca.dt$n_edo
plot_ly(data = ring.pc.dt, x = ~PC1, y = ~PC2, z = ~PC3, color = ~factor(n_edo))

ring.pc.variance <- (ring.pc$sdev)^2
ring.proportion.variance.explained <- ring.pc.variance / sum(ring.pc.variance)
plot(ring.proportion.variance.explained)
# Great.  Basically all the variance is in the first two dimensions.

