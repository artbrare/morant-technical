library(dplyr)
library(ggplot2)
library(vroom)
library(forcats)
library(purrr)
library(shiny)
injuries <- vroom::vroom("injuries.tsv")

products <- vroom::vroom("products.tsv")

population <- vroom::vroom("population.tsv")

prod_codes <- setNames(products$prod_code, products$title)


ui <- fluidPage(
  fluidRow(
    column(8,
           selectInput("code", "Product",
                       choices = setNames(products$prod_code, products$title),
                       width = "100%"
           )
    ),
    column(2, selectInput("y", "Y axis", c("rate", "count")))
  ),
  fluidRow(
    column(4, tableOutput("diag")),
    column(4, tableOutput("body_part")),
    column(4, tableOutput("location"))
  ),
  fluidRow(
    column(12, plotOutput("age_sex"))
  )
)


server <- function(input, output, session) {
  selected <- reactive(injuries %>% filter(prod_code == input$code))
  
  output$diag <- renderTable({
    count(selected(), diag, wt = weight, sort = TRUE)
  }, width = "100%")
  
  output$body_part <- renderTable({
    count(selected(), body_part, wt = weight, sort = TRUE)
  }, width = "100%")
  
  output$location <- renderTable({
    count(selected(), location, wt = weight, sort = TRUE)
  }, width = "100%")
  
  summary <- reactive({
    selected() %>%
      count(age, sex, wt = weight) %>%
      left_join(population, by = c("age", "sex")) %>%
      mutate(rate = n / population * 1e4)
  })
  
  output$age_sex <- renderPlot({
    if (input$y == "rate") {
      ggplot(summary(), aes(age, rate, colour = sex)) +
        geom_line(na.rm = TRUE) +
        labs(y = "Lesiones por cada 10.000 personas")
    } else {
      ggplot(summary(), aes(age, n, colour = sex)) +
        geom_line() +
        labs(y = "Número estimado de lesiones")
    }
  })
}

shinyApp(ui, server)