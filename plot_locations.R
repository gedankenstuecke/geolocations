# load libraries
library(ggplot2)
library(ggthemes)

Sys.setlocale("LC_CTYPE", "en_US.UTF-8")
Sys.setlocale("LC_ALL", "en_US.UTF-8")

# read arguments
args <- commandArgs(trailingOnly = TRUE)
# get all file names
files <- list.files(path=args[1],pattern=paste("*.",args[2],sep=""),full.names=TRUE)
# convert into single data frame
datalist = lapply(files, function(x){read.csv(file=x,header=T,sep="|",quote="")})
merged <- Reduce(function(x,y) {merge(x,y,all=TRUE)}, datalist)

# simple data cleanup -> remove (0,0) locations
merged <- subset(merged,merged$lat != 0.0)
# generate world map
world <- map_data("world")

plot <- ggplot(world, aes(x=long, y=lat, group=group)) + geom_path()

plot <- plot + scale_x_continuous(limits=c(min(merged$long,na.rm=T)-1,max(merged$long,na.rm=T)+1))
plot <- plot + scale_y_continuous(limits=c(min(merged$lat,na.rm=T)-1,max(merged$lat,na.rm=T)+1))
plot <- plot + coord_map()
plot <- plot + geom_segment(data=merged,aes(y=last_lat,x=last_long,yend=lat,xend=long,color=user,group=NULL),alpha=0.3)
plot <- plot + theme_tufte()+ theme(text=element_text(family="Helvetica"))
ggsave("plot_travel_routes.pdf",width=20, height=10)

merged$lat_round <- round(merged$lat,digit=2)
merged$long_round <- round(merged$long,digit=2)
merged_table <- table(merged$lat_round,merged$long_round,merged$user)
merged_table.m <- as.data.frame(merged_table)
merged_table.m <- subset(merged_table.m,merged_table.m$Freq >0)
merged_table.m$Var2 <- as.numeric(as.character(merged_table.m$Var2))
merged_table.m$Var1 <- as.numeric(as.character(merged_table.m$Var1))

plot <- ggplot(world, aes(x=long, y=lat, group=group)) + geom_path()
plot <- plot + scale_x_continuous(limits=c(min(merged$long,na.rm=T)-1,max(merged$long,na.rm=T)+1))
plot <- plot + scale_y_continuous(limits=c(min(merged$lat,na.rm=T)-1,max(merged$lat,na.rm=T)+1))
plot <- plot + coord_map()
plot <- plot + geom_point(data=merged_table.m,
        aes(x=Var2,
            y=Var1,
            size=log(Freq),alpha=log(Freq),
            color=Var3,group=NULL))
plot <- plot + scale_color_discrete("user")
plot <- plot + theme_tufte() + theme(text=element_text(family="Helvetica"))

ggsave("plot_heatmapish.pdf",width=20, height=10)
