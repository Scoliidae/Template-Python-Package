' Uses the Windows Script Host Run() to call headless batch
'note   intWindowStyle : 0 means "invisible windows"
'   bWaitOnReturn : false means your first script does not need to wait for your second script to finish
CreateObject("Wscript.Shell").Run "PKG_DIR\start.cmd MODE=hybrid", 1, True
