s=""        
with open("./requirements.txt", "r") as f:
    #print (*("[" + line.split(" ")[0].strip() + "]\n" for line in f if line.strip() != "" and line.strip()[0] != "#"))
    #* unpacks teh generator iterator
    for line in f:
        if line.strip() != "" and line.strip()[0] != "#":
            s = s + "import " + line.split(" ")[0].strip().replace("-","_").replace("python_dotenv","dotenv") + "\n"
print("Checking " +s)
print("-----------------------------------------------------")
s= 'print("Starting requiremnets check")\n' + s + 'print("All requiremnets check completed succesfully!!!")'
dynamic_code = s #"print('Hello, dynamically generated code!')"
try:
    exec(dynamic_code)
except Exception as e:
    print(f"Not all installs successful. Maybe again try `pip install-r requirements.txt`  : {e}")     
    '''import linecache
    tb = sys.exc_info()[2]
    filename = tb.tb_frame.f_code.co_filename
    lineno = tb.tb_lineno
    line = linecache.getline(filename, lineno)
    print(str(lineno) + "---" +line)'''