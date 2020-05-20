# Title     : Rgraphy2
# Objective : API to graphy2.py
# Created by: Samuel Baker
# Created on: 19/05/2020

validatePath <- function(python_path){
  graphy_path <- paste(c(python_path, "/Lib/site-packages/graphy2/__init__.py"), collapse="") # TODO This needs to be to the API

  if (file.exists(graphy_path)){
    return(graphy_path)
  }else{
    stop(paste0("Failed to find ", graphy_path, "
    This could be because the python path you provided is not valid or that you haven't installed graphy2
    You can install graphy2 from the terminal as python -m pip install graphy2"))

  }

}


scatterPlot <- function (python_path, data, write_directory, figure_name, x_variable, y_variable,
                         graident_variable=FALSE, size_variable=FALSE, custom_ranking=FALSE, style_sheet=FALSE) {

  api_path <- validatePath(python_path)

  system2("python", args=c(api_path, "scatter_plot", data,
                           write_directory, figure_name, style_sheet, x_variable, y_variable, graident_variable,
                           size_variable, custom_ranking))

}

