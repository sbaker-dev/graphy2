program graphy2_scatter
	quietly{
	args python_path data_path x_variable y_variable ///
	graident_variable size_variable custom_ranking ///
	figure_name style_sheet write_directory
	
	if "`python_path'" == "" {
		display as error "Path to graphy2.api required to run"
		display as error "please check graphy2_scatter2 to ensure that you"  ///
		"are submiting the right number and order of arguments"
		exit 111
	}
	
	if "`data_path'" == "" {
		display as error "Path to data required to run"
		display as error "please check graphy2_scatter2 to ensure that you"  ///
		"are submiting the right number and order of arguments"
		exit 111
	}
	
	if "`write_directory'" == "" {
		display as text "Using default working direcotry"
		local write_directory `c(pwd)'
	}
		

	// these should be loops but im uncertain how to do that in stat a given 
	// forvalues and foreach seem to be expecting actual names of variables in
	// the data table not tempnames
	if "`figure_name'" == "" local figure_name "Graphy_Stata_Figure"
	if "`graident_variable'" == "" local graident_variable "FALSE"
	if "`size_variable'" == "" local size_variable "FALSE"
	if "`custom_ranking'" == "" local custom_ranking "FALSE"
	if "`style_sheet'" == "" local style_sheet "FALSE"
	
	#delimit;
	shell python `python_path' "scatter_plot" `data_path' `write_directory'
	`figure_name' `style_sheet' `x_variable' `y_variable' `graident_variable'
	`size_variable' `custom_ranking';
	#delimit cr
	}
end