  library(ggplot2)
  library(extrafont)
  loadfonts()
  total_btc <- read.csv("C:/Honors_Thesis/total-bitcoins.csv")
  total_btc$Date <- as.Date(total_btc$Date,format="%m/%d/%Y")
  total_btc$Produced <- total_btc$Produced/1000000
  
  total_bitcoins <- ggplot(data=total_btc,aes(x=total_btc$Date,y=total_btc$Produced))+
            geom_line(color='red') +
            geom_hline(yintercept = c(0))+
            geom_vline(xintercept = as.numeric(as.Date('2009-01-03')))+
            scale_x_date(limits = as.Date(c('2009-01-03','2017-03-02')),expand=c(0,0.5))+
            scale_y_continuous(limits = c(0,20),expand = c(0,0.75))+
            labs(x="Year",y="Bitcoin Produced (MM)")+
            theme(panel.background = element_rect(fill = "white",
                                          colour = "white",
                                          size = 0.5, linetype = "solid"),
                  panel.grid.major.y = element_line(size = 0.5, linetype = 'solid',
                                                    colour = "grey")) +
            ggtitle("Total Bitoin Created") +
            theme(axis.text = element_text(family="CM Roman", size = 14))+
    theme(plot.title = element_text(family = "CM Roman", color="black", size=22, hjust=.5)) +
    theme(axis.title = element_text(family = "CM Roman", color="black", face="bold", size=18))#   
   #grid(col = "lightgray", lty = "dotted",
  #       lwd = par("lwd"), equilogs = TRUE)
  ggsave("Total_Bitcoins_Produced2_1.pdf", total_bitcoins, width=5, height=4)
