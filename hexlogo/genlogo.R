library(pacman)
p_load(hexSticker)
p_load(ggplot2)
p_load(RColorBrewer)
p_load(ggridges)
p_load(tis)


d <- diamonds[sample(x = 1:nrow(diamonds), 800), ]
p <- ggplot(d, aes(x = carat, y = price, color=clarity)) + geom_point(alpha=0.2)
p <- p + theme_void() + theme_transparent() + theme(legend.position = "none") 

s <- sticker(p, package="Econometria", p_size=18, s_x=1.2, s_y=.75, s_width=1.3, s_height=1,
        filename="../teaching/logo/econometria.png", h_color = "darkcyan", url = "gragusa.org/econometria",h_size = 1.1, h_fill = "black")

p <- ggplot(lincoln_weather, aes(x = `Mean Temperature [F]`, y = Month, fill = stat(x))) +
  geom_density_ridges_gradient(scale = 3, rel_min_height = 0.01, lwd=0.4, color = "gray") +
  scale_fill_gradient(high = "#006778", low = "#aaa38c") + theme_void() + theme_transparent() + theme(legend.position = "none") 

s <- sticker(p, package="Adv metrics", p_size=16, s_x=1.2, s_y=.75, s_width=1.3, s_height=1,
             filename="../teaching/logo/advmetrics.png", h_color = "darkcyan", url = "gragusa.org/advmetrics",h_size = 1.1, h_fill = "#006778")

set.seed(2123)
x <- arima.sim(n = 163, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)),
          sd = sqrt(0.21796))
z <- rnorm(n = 163, mean = 0, sd = 0.2)
z1 <- z - .3
z2 <- z + .3

df <- data.frame(x=x, z = z, z1 = z1, z2 = z2)


p <- ggplot(df, aes(y = x, x = 1:163)) + geom_line(col = "darkred") +  theme_void() + theme_transparent() + theme(legend.position = "none") 
p<- p + geom_line(aes(y=z), color = "slategray") + 
  geom_line(aes(y=z1), color = "slategray", linetype=2) + 
  geom_line(aes(y=z2), color = "slategray", linetype=2)



s <- sticker(p, package="Macroeconometrics", p_size=13, s_x=1., s_y=.75, s_width=1.3, s_height=1,
             filename="../teaching/logo/comptools.png", h_color = "darkcyan", url = "gragusa.org/comptools",h_size = 1.1, h_fill = "darkgray")


