  library(scales)
  library(ggplot2)
  library(extrafont)
  loadfonts()
  arbEx <- read.csv("C:/Honors_Thesis/ArbExample.csv")
  arbEx$'Exchange 1' <- arbEx$A
  arbEx$'Exchange 2' <- arbEx$B
  
  arbEx$Date <- as.Date(arbEx$Date)
  
  arbExample <- ggplot(data=arbEx,aes(x=arbEx$Date,y=arbEx$'Exchange 1'))+
    geom_line(color='darkgreen') +
    geom_line(aes(x=arbEx$Date,y=arbEx$'Exchange 2',color='Exchange 2'),color='red') +
    geom_hline(yintercept = c(0))+
    geom_segment(aes(x=as.Date('2014-1-25'),y=12,xend=as.Date('2014-1-24'),yend=13),color='grey')+
    geom_segment(aes(x=as.Date('2014-1-25'),y=10,xend=as.Date('2014-1-24'),yend=9),color='grey')+
    geom_point(aes(x=as.Date('2014-1-25'),y=10),color='darkgreen')+
    geom_point(aes(x=as.Date('2014-1-25'),y=12),color='red')+
    geom_vline(xintercept = as.numeric(as.Date('2014-01-13')))+
    annotate("text", x=as.Date('2014-1-24'), y=8, label= "Buy on Exchange 1") +
    annotate("text", x=as.Date('2014-1-26'), y=11.25, label= "}", size = 9) +
    annotate("text", x=as.Date('2014-1-28'), y=11, label= "Spread") +
    annotate("text", x=as.Date('2014-1-24'), y=14, label= "Sell on Exchange 2") + 
    scale_x_date(limits = as.Date(c('2014-01-13','2014-01-30')),expand=c(0,0.5))+
    scale_y_continuous(limits = c(0,20),expand = c(0,0.75),labels=dollar)+
    labs(x="Date",y="Price")+
    theme(panel.background = element_rect(fill = "white",
                                          colour = "white",
                                          size = 0.5, linetype = "solid"),
          panel.grid.major.y = element_line(size = 0.5, linetype = 'solid',
                                            colour = "white")) +
    ggtitle("Stock A on Two Exchanges:") +
    theme(axis.text = element_text(family="CM Roman", size = 14))+
    theme(plot.title = element_text(family = "CM Roman", color="black", size=22, hjust=.5)) +
    theme(axis.title = element_text(family = "CM Roman", color="black", face="bold", size=18))#   
  #grid(col = "lightgray", lty = "dotted",
  #       lwd = par("lwd"), equilogs = TRUE)
  ggsave("ArbExample.pdf", arbExample, width=5, height=4)
