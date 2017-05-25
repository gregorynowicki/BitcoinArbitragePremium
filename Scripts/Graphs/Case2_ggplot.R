library(ggplot2)
library(extrafont)
library(scales)
loadfonts()
case1_1d <- read.csv("C:/Honors_Thesis/Case1_1D.csv")
case1_2d <- read.csv("C:/Honors_Thesis/Case1_2D.csv")
case1_3d <- read.csv("C:/Honors_Thesis/Case1_3D.csv")
case2_1d <- read.csv("C:/Honors_Thesis/Case2_1D.csv")
case2_2d <- read.csv("C:/Honors_Thesis/Case2_2D.csv")
case2_3d <- read.csv("C:/Honors_Thesis/Case2_3D.csv")

case1_1d$Date <- as.Date(case1_1d$Date)
case1_2d$Date <- as.Date(case1_2d$Date)
case1_3d$Date <- as.Date(case1_3d$Date)

case2_1d$Date <- as.Date(case2_1d$Date)
case2_2d$Date <- as.Date(case2_2d$Date)
case2_3d$Date <- as.Date(case2_3d$Date)


# case1_1d$Return <- case1_1d$Return*100
# case1_2d$Return <- case1_2d$Return*100
# case1_3d$Return <- case1_3d$Return*100
# case2_1d$Return <- case2_1d$Return*100
# case2_2d$Return <- case2_2d$Return*100
# case2_3d$Return <- case2_3d$Return*100



returns <- ggplot(data=case2_1d,aes(Date,Return))+
  geom_line(aes(case2_1d$Date,case2_1d$Return),color='red') +
  geom_line(aes(case2_2d$Date,case2_2d$Return),color='blue')+
  geom_line(aes(case2_3d$Date,case2_3d$Return),color='black')+
  geom_hline(yintercept = c(0))+
  geom_vline(xintercept = as.numeric(as.Date('2014-03-01')))+
  scale_x_date(limits = as.Date(c('2014-03-01','2017-03-02')),expand=c(0,0))+
  scale_y_continuous(limits = c(0,1),expand = c(0,0),labels = percent)+
  labs(x="Year",y="Monthly Return")+
  theme(panel.background = element_rect(fill = "white",
                                        colour = "white",
                                        size = 0.5, linetype = "solid"),
        panel.grid.major.y = element_line(size = 0.5, linetype = 'solid',
                                          colour = "grey")) +
  ggtitle("Case 2: Monthly Returns From March 2014") +
  theme(axis.text = element_text(family="CM Roman", size = 14))+
  theme(plot.title = element_text(family = "CM Roman", color="black", size=22, hjust=.5)) +
  theme(axis.title = element_text(family = "CM Roman", color="black", face="bold", size=18)) +
  scale_colour_manual(values=c("red","blue","black"))#   
#grid(col = "lightgray", lty = "dotted",
#       lwd = par("lwd"), equilogs = TRUE)
ggsave("Case2_MonthlyReturnP2.pdf", returns, width=10, height=6)
