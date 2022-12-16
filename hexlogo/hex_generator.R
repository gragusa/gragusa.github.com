## Hexsticker
library(pacman)

p_load(hexSticker)
p_load(ggplot2)
p_load(png)
p_load(grid)
p_load(RColorBrewer)

p_load(showtext)
## Loading Google fonts (http://www.google.com/fonts)
font_add_google("Gochi Hand", "gochi")
## Automatically use showtext to render text for future devices
showtext_auto()


porpora <- "#AE262B"
porpora_tiro <- "#31002F"
porpora_chiaro <- "#4B0049"
beige <- "#F5F5DC"

set.seed(1)
x <- runif(20)
y <- x + runif(20)
df <- data.frame(y=y,x=x)

df[which.max(df[,2]), "x"] <- 1
df[which.min(df[,2]), "x"] <- 0

df$show <- 1

df[which.min(df[,2]), "show"] <- FALSE
df[which.max(df[,2]), "show"] <- FALSE


img <- readPNG("lm.png", native=TRUE)
g <- rasterGrob(img)


p <-  ggplot(df, aes(y=y, x=x)) + 
  geom_point(aes(alpha = factor(show)), color = "slategray1", size=.2) + 
  geom_smooth(method="lm", level = 0.85, color=porpora_tiro, fill="gray", alpha=0.15, lty=3, lwd=.2, fullrange=TRUE) +
  annotation_custom(g, xmin=0.23, xmax=0.77, ymin=0.4, ymax=0.6) + 
  scale_alpha_manual(values = c(0.05, 1)) + 
  theme_transparent() + 
  theme_void() + 
   theme(legend.position = "none")

sticker(p, package="Econometria 1", p_size=5, p_color = "turquoise3", p_family="gochi", s_x=1, s_y=.8, s_width=1.8, s_height=1,
        filename="../teaching/logo/econometria1.png", h_fill = "#495057", spotlight = TRUE, h_color="mistyrose4")


img <- readPNG("Caduceus3.png", native=TRUE)
g <- rasterGrob(img)

p2 <- ggplot(df, aes(y=y, x=-x)) + 
  geom_point(aes(alpha = factor(show)), color = "slategray1", size=.2) + 
  geom_smooth(level = 0.85, color=porpora_tiro, fill="gray", alpha=0.15, lty=3, lwd=.2, fullrange=TRUE) +
  scale_alpha_manual(values = c(0.05, 1)) + 
  theme_transparent() + 
  theme_void() +
  annotation_custom(g, xmin=-Inf, xmax=+Inf, ymin=-Inf, ymax=+Inf) +
  theme(legend.position = "none")

sticker(p2, package="Health Econometrics", p_size=4, p_color = "turquoise3", p_family="gochi", s_x=1, s_y=.8, s_width=1.8, s_height=1,
        filename="../teaching/logo/healthmetrics.png", h_fill = "#495057", spotlight = TRUE,  h_color="mistyrose4")

set.seed(7875)
df <- data.frame(x=cut(rexp(250, rate = .51), 6))


font_add_google(name = "Cabin", family = "cabin")
## Automatically use showtext to render text for future devices
showtext_auto()



# p <- ggplot(df, aes(x=x, fill=factor(x))) +  scale_fill_brewer(palette = "Blues")  + theme_transparent() + 
#   theme_void() + theme(legend.position = "none")
# 
# sticker(p, package="GR", p_size=16, p_color = "#AE262B", p_x = 1, p_y=1, p_family="cabin", s_x=0, s_y=0, s_width=1, s_height=1,
#         filename="~/mylogo.png", h_fill = "#325d88", spotlight = FALSE,  h_color="mistyrose4")
# 
# 
# library(extrafont)
# library(ggplot2)
# if( 'xkcd' %in% fonts()) {
#   p <-  ggplot() + geom_point(aes(x=mpg, y=wt), data=mtcars) + 
#     theme(text = element_text(size = 16, family = "xkcd"))
# } else  {
#   warning("Not xkcd fonts installed!")
#   p <-  ggplot() + geom_point(aes(x=mpg, y=wt), data=mtcars) 
# }
# p
# 
# 
# 
