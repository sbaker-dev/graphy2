# Title     : Rgraphy2
# Objective : API to graphy2.py
# Created by: Samuel Baker
# Created on: 19/05/2020

validatePath <- function(python_path){
  graphy_path <- paste(c(python_path, "/Lib/site-packages/graphy2/api.py"), collapse="")

  if (file.exists(graphy_path)){
    return(graphy_path)
  }else{
    stop(paste0("Failed to find ", graphy_path, "
    This could be because the python path you provided is not valid or that you haven't installed graphy2
    You can install graphy2 from the terminal as python -m pip install graphy2"))

  }

}

#' Creation of Scatter plot using Seaborns ScatterPlot Function
#'
#' @param python_path The path to your python installation
#' @param data The path to your data directory
#' @param write_directory The path you want to write the plot out to
#' @param figure_name The name of the png file you want to use, defaults to GraphyFigure
#' @param x_variable The x variable name from your data column header names you want to use as the x variable
#' @param y_variable The y variable name from your data column header names you want to use as the y variable
#' @param graident_variable The varaible to use to add a graident of colour to the graph, optional
#' @param size_variable The varaible to control the size of the points in the scatter, optional
#' @param custom_ranking A custom list of rankings to order the variables, optional
#' @return None
#'
#' @export
scatterPlot <- function (python_path, data, write_directory, figure_name, x_variable, y_variable,
                         graident_variable=FALSE, size_variable=FALSE, custom_ranking=FALSE, style_sheet=FALSE) {

  api_path <- validatePath(python_path)

  system2("python", args=c(api_path, "scatter_plot", data,
                           write_directory, figure_name, style_sheet, x_variable, y_variable, graident_variable,
                           size_variable, custom_ranking))

}

