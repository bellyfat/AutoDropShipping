# Projects

**** ReamMe ****

Inside the main ZIP there are 3 folders:
	1. GuiFinalProj - The GUI.
	2. NFH_MembershipProblem_Solver - A DLL for external using.
	3. SoftwareEngineeringProject - The same code as NFH_MembershipProblem_Solver, but with a debugger main.

You have 2 options of running our project:
	1. With GUI (requiers pathes changing).
	2. Without GUI (just running).

For option number 1: (Running the project with GUI)
	1. Change the path at NFH_MembershipProblem_Solver package:
		Go to Header.h at NFH_MembershipProblem_Solver and change 'const char* nfh_file_name' and 'const char* nfa_file_name' to a
		path you like. Build NFH_MembershipProblem_Solver again (by right click on NFH_MembershipProblem_Solver package and click build).
	2. Change Path.cs class's attribute 'public static string path' at FinalProjectGUI to the path of your desktop.
	3. In FinalProjectGUI, in class ViewResultWin.cs, change the path in line 17 ([DllImport(...)] to the path of NFH_MembershipProblem_Solver.
	4. Build FinalProjectGUI again (by right click on FinalProjectGUI package and click build).
	5. Build a new solution by right click on the solution and click build solution.
	
	Notice: The GUI will ask for NFA and NFH text files - This files is inside the main ZIP.

For option number 2: (Running the project without GUI)
	Just open SoftwareEngineeringProject.

Thank you.
