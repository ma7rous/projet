library(shiny)
library("shinydashboard")
library(randomForest)
library("FactoMineR")
library("factoextra")
library(NbClust)


source("source_coef.R", local = TRUE)

shiny::runApp(
  list(
    ui = dashboardPage( #l'interface graphique
      dashboardHeader(title = "Strivee"), #le titre de l'application
      dashboardSidebar(fileInput("file","Upload the file"), # le menu des choix
                       h5("Max file size to upload is 5 MB"), 
                       radioButtons("sep","separator",choices = c(Comma = ',',Period = ".",Tilde = "~",Minus = "-")), #les choix des separateurs entre des differents variables
                       checkboxInput("header","Header?"), # On choisit si on inclut lapremiere ligne (nom des variables) ou pas
                       textInput("identifiant","Identification",1), #Entrez votre identifiant (doit etre un chiffre entre 1 et le nombre des lignes)
                       submitButton("update")),
      dashboardBody(
        tabsetPanel(
          tabPanel(h4("DATA BASE"),
                   tabsetPanel(
                     tabPanel(tableOutput("input_file")) #on utilise un tableOutput pour afficher la base des donnees
                   )),
          
          tabPanel(h4("IMPUTED DATA BASE"),
                   tabsetPanel(
                     tabPanel(tableOutput("test"))
                   )),
          
          tabPanel(h4("SCORE"),
                   tabsetPanel(
                     tabPanel(uiOutput("matrix")) #on utilise un uiOutput pour afficher le tableau des scores des groupes musculaires
                   )),
          tabPanel(h4("DATA BASE MUSCLES"),
                   tabsetPanel(
                     tabPanel(tableOutput("df_muscle")) #on utilise un tableOutput pour afficher la base des donnees
                   )),
          tabPanel(h4("PCA"),
                   tabsetPanel(
                     tabPanel(plotOutput("variables")),
                     tabPanel(plotOutput("individus")),
                     tabPanel(plotOutput("individus1")) #on utilise des plotOutput pour afficher les differents graphes des ACP, Kmeans et la classification hierarchique
                   )),
          tabPanel(h4("PCA MUSCLES"),
                   tabsetPanel(
                     tabPanel(plotOutput("variables2")),
                     tabPanel(plotOutput("individus2")),
                     tabPanel(plotOutput("individus3"))
                   )),
          tabPanel(h4("ANOVA"),
                   tabsetPanel(
                     tabPanel(textInput("modstr","Enter Model: ", "globalFL ~ sex"), #on utilise un textInput pour entrer les differents modeles possibles pour effectuer l'ANOVA
                              submitButton("Update View"),
                              verbatimTextOutput("anovatable")) #on utilise des verbatimTextOutput pour afficher les resultats d'anova ainsi que le TukeyHSD test
                   ))
          
        )
      )
    )
    , 
    server = function(input,output){ # dans cette partie (server) on implemte les calculs des differents fonctions pour importer et nettoyer les donnes, et le calcul des methodes statistiques   
      
      # une fonction qui lit et rearranger les donnees
      the_data_fn <- reactive({
        file_to_read = input$file #upload le fichier
        if(is.null(file_to_read)){
          return()
        }
        df = read.table(file_to_read$datapath, sep = input$sep, header = input$header) #on lit le fichier en prenant en consideration les seperateurs et le header
        df$userID <- 1:nrow(df) #on change le noms des individus a nrow-uplet
        df = df[,c(1,2,3,4,5,7,9,11,13,15,17,19,21,
                   23,25,27,29,31,33,35,37,
                   39,41,43,45,47,49,51,53,55,57,58)] #on rearrange les colones
        colnames(df) <- c('userID','poids','taille','sex','globalFL','Back.Squat','Front.Squat','Overhead.squat','Deadlift','Sumo.Deadlift',
                          'Power.Clean','Squat.clean','Power.snatch','Squat.Snatch','Bench.Press',
                          'Shoulder.Press','Push.Press','Jerk','Toes.to.bar','Pull.ups.strict','Pull.ups',
                          'Chest.to.bar.Strict','Chest.to.bar','HSPU.Strict','HSPU','Bar.MU','Ring.MU','Bar.dips',
                          'Push.ups','L.sit','Double.unders','age')
        
        col_order <- c('userID','globalFL','age','poids','taille','sex','Back.Squat','Front.Squat','Overhead.squat','Deadlift','Sumo.Deadlift',
                       'Power.Clean','Squat.clean','Power.snatch','Squat.Snatch','Bench.Press',
                       'Shoulder.Press','Push.Press','Jerk','Toes.to.bar','Pull.ups.strict','Pull.ups',
                       'Chest.to.bar.Strict','Chest.to.bar','HSPU.Strict','HSPU','Bar.MU','Ring.MU','Bar.dips',
                       'Push.ups','L.sit','Double.unders')
        df <- df[, col_order]
        df$sex <- as.factor(df$sex)
        df$poids <- as.numeric(as.character(df$poids)) / 10 #la base de donnees fournie contient des valeurs fausses pour les poids, il suffit de diviser par 10  
        return(df)
      })
      
      #Affichage de notre base de donnees
      output$input_file <- renderTable({
        the_data_fn()
      })
      
      # on impute la base par la methode des forets aleatoires en utilisant la fontion rfImpute de la librairie randomForest
      the_imputed_data_fn <- reactive({       
        df <- the_data_fn()
        df[df == 0] <- NA
        set.seed(123)
        data.imputed <- rfImpute(globalFL ~ ., data = df[,-c(6)], iter=5) 
        return(data.imputed)
      })
      #Affichage de la base de donnees imputee
      output$test <- renderTable({ 
        the_imputed_data_fn()
      })
      
      #Creation de la base de donnees des groupes musculaires
      the_muscle_data_fn <- reactive({ 
        df <- the_data_fn()
        result <-  numeric()
        for (i in (1:nrow(df))) {
          user <- df[which(df$userID == i), ]
          userNumeric <- as.numeric(user[1,])
          vecteur2 <- c()
          for (l in (1:21)) {
            j = 7:32
            vecteur2 <- c(vecteur2,abs(sum(abs(userNumeric[j]-userNumeric[2])*coef_df[,l])/moy))
          }
          result <-  c(result,vecteur2)
        }
        
        data_muscle <- split(result, ceiling(seq_along(result)/21))
        data_muscle <- as.data.frame(data_muscle)
        data_muscle <- as.data.frame(t(data_muscle))
        colnames(data_muscle) <- c("Sangle Abdominale","Spinaux (érecteur du rachis)","Fessiers",
                                   "Ischios","Quadriceps","Adducteurs",
                                   "Flechisseurs de Hanche","Mollets","Pectoraux (faisseau claviculaire)",
                                   "Pectoraux (faisceau sternaul)","Grand Dorsal - Grand Rond","Deltoïdes Antérieur",
                                   "Deltoïdes Médian","DeltoIde Postérieur","Rotateurs de la coiffe",
                                   "Trapèzes inférieurs","Fixateurs d'Omoplate (trapèze milieux)",
                                   "Trapèzes supérieurs","Triceps","Biceps",
                                   "Avant-Bras")
        rownames(data_muscle) <- c(1:nrow(data_muscle))
        return(data_muscle)
      })
      
      #Affichage de la base de donnees des groupes musculaires
      output$df_muscle <- renderTable({ 
        the_muscle_data_fn()
      })
      
      
      #creation d'une base de donnees pour l'ANOVA
      the_anova_data_fn <- reactive({
        anova.data <- the_imputed_data_fn()
        #on cree une nouvelle variable qualitative "performance" base sur la variable "globalFL"
        anova.data$performance <- cut(anova.data$globalFL,
                                      breaks = c(0,mean(anova.data$globalFL),0.8*max(anova.data$globalFL),max(anova.data$globalFL)),
                                      labels = c("non performant","assez performant","performant"))
        DATA = the_data_fn()
        anova.data <- cbind(anova.data, DATA)
        anova.data <- anova.data[,-c(33,34,35,37,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64)]
        col_order2 <- c('userID','globalFL','performance','age','poids','taille','sex','Back.Squat','Front.Squat','Overhead.squat','Deadlift','Sumo.Deadlift',
                        'Power.Clean','Squat.clean','Power.snatch','Squat.Snatch','Bench.Press',
                        'Shoulder.Press','Push.Press','Jerk','Toes.to.bar','Pull.ups.strict','Pull.ups',
                        'Chest.to.bar.Strict','Chest.to.bar','HSPU.Strict','HSPU','Bar.MU','Ring.MU','Bar.dips',
                        'Push.ups','L.sit','Double.unders')
        anova.data <- anova.data[, col_order2]
        return(anova.data)
      })
      
      
      ######################  calcul des scores des groupes musculaires:
      
      output$matrix <- renderTable({
        #on cree une base de donnees df a partir de la base de donnees imputee et on enleve garde que les variables globalFL, userID et ceux des mouvements 
        df <- the_data_fn()
        #la fonction suivante correspont l'utilisateur a ses 'scores' (dans chaque mouvement)
        identification <- function(user){
          for (k in (1:nrow(df))) {
            if (k == user) {
              FindUser <- df[which(df$userID == k), ]
            }
          }
          return(FindUser)
        }
        
        UserFound <- identification(input$identifiant)
        UserFoundNumeric <- as.numeric(UserFound[1,])
        
        vecteur <- c()
        for (l in (1:21)) {
          j = 7:32
          vecteur <- c(vecteur,sum(abs((UserFoundNumeric[j]-UserFoundNumeric[2])*coef_df[,l]))/moy) # ce vecteur contient les scores pour tout les groupes musculaires en utilisant la formule trouve dans le rapport
        }
        
        matrix <-  matrix(vecteur,ncol=1,nrow=21) # le tableau des scores
        colnames(matrix) <- c("Score")
        rownames(matrix) <- c("Sangle Abdominale","Spinaux (érecteur du rachis)","Fessiers",
                              "Ischios","Quadriceps","Adducteurs",
                              "Flechisseurs de Hanche","Mollets","Pectoraux (faisseau claviculaire)",
                              "Pectoraux (faisceau sternaul)","Grand Dorsal - Grand Rond","Deltoïdes Antérieur",
                              "Deltoïdes Médian","DeltoIde Postérieur","Rotateurs de la coiffe",
                              "Trapèzes inférieurs","Fixateurs d'Omoplate (trapèze milieux)",
                              "Trapèzes supérieurs","Triceps","Biceps",
                              "Avant-Bras")
        matrix
      }, rownames = TRUE)
      
      ###################### ACP MUSCLE :
      
      output$variables2 <- renderPlot({data_muscle <- the_muscle_data_fn()
                                       res.pca <- PCA(data_muscle[,-1], scale.unit = TRUE, graph = F)
                                       var <- get_pca_var(res.pca)
                                       fviz_pca_var(res.pca, col.var = "black")}, height = 400, width = 600)
      output$individus2 <- renderPlot({data_muscle <- the_muscle_data_fn()
                                       res.pca <- PCA(data_muscle[,-1], scale.unit = TRUE, graph = F)
                                       ind <- get_pca_ind(res.pca)
                                       fviz_pca_ind(res.pca)}, height = 400, width = 600)
      
      output$individus3 <- renderPlot({res.pca2 <- PCA(data_muscle[,-1], scale.unit = TRUE, graph = F) 
                                       fviz_pca_ind(res.pca2,geom.ind = "point", addEllipses = T, col.ind = data_muscle$performance,legend.title = "Groups")}, height = 400, width = 600)
      
      ###################### Kmeans MUSCLE:
      
      # output$Elbow <- renderPlot({fviz_nbclust(data_muscle[-1], kmeans, method = "wss") + labs(subtitle = "Elbow method")}, height = 400, width = 600)
      # output$centre_groupe2 <- renderPlot({km.res <- kmeans(data_muscle[-1], 3, nstart = 25)
      #                                      fviz_cluster(km.res, data =  data_muscle[-1])}, height = 400, width = 600)
      
      
      ###################### ACP :
      
      output$variables <- renderPlot({data.imp <- the_imputed_data_fn()
                                      res.pca2 <- PCA(data.imp[,-c(2,32)], scale.unit = TRUE, graph = F)
                                      fviz_pca_var(res.pca2, col.var = "black")}, height = 400, width = 600)
      output$individus <- renderPlot({data.imp <- the_imputed_data_fn()
                                      res.pca2 <- PCA(data.imp[,-c(2,32)], scale.unit = TRUE, graph = F)
                                      fviz_pca_ind(res.pca2,geom.ind = "point", # show points only (nbut not "text")
                                                   col.ind = data_muscle$performance, # color by groups
                                                   addEllipses = T, # Concentration ellipses
                                                   legend.title = "Groups")}, height = 400, width = 600)
      output$individus1 <- renderPlot({data.imp <- the_imputed_data_fn()
      res.pca2 <- PCA(data.imp[,-c(2,32)], scale.unit = TRUE, graph = F)
        fviz_pca_ind(res.pca2)}, height = 400, width = 600)
      
      
      
      
      ###################### Kmeans :
      
      # output$gourpe_individus <- renderPlot({km.res2 <- kmeans(data.imputed[,-c(1,2,32)], 3, nstart = 25)
      #                                        fviz_cluster(km.res2, data =  data.imputed[,-c(1,2,32)])}, height = 400, width = 600)
      # 
      ###################### ANOVA :
      
      output$anovatable <- renderPrint({
        dataset=the_anova_data_fn()
        aov.model<-aov(formula(input$modstr), data=dataset)
        print(aov.model)
        br()
        br()
        print(summary(aov.model))
        cat("Coefficients"); cat("\n")
        print(aov.model$coefficients)
        br()
        cat(paste("--------------------------------------------------","\n\n"))
        print(model.tables(aov.model, "means"))
        cat(paste("--------------------------------------------------","\n\n"))
        TukeyHSD(aov.model)
        
      }) 
      
    }
  )
)
