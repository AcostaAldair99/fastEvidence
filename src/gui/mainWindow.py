from dependecies import *

jsonFilepath = os.getcwd()+"\src\config\settings.json"

class mainWindow():

  def __init__(self,root):
    self.root = root
    self.evidence = ""
    self.weStart = False
    setWindow(self.root,"Fast Evidence",400,200,"CENTER")

    self.mainFrame = ttk.Frame(root)
    self.mainFrame.columnconfigure(0, weight=1,pad=10)
    self.mainFrame.columnconfigure(1, weight=3,pad=10)

    self.mainFrame.rowconfigure(0,weight=1,pad=10)
    self.mainFrame.rowconfigure(1,weight=1,pad=10)
    self.mainFrame.rowconfigure(2,weight=1,pad=10)


    #Path Entry
    ttk.Label(self.mainFrame, text='* Directory:',anchor='w').grid(column=0, row=0,sticky='w')
    self.dirPathText= tk.StringVar()
    self.dirPath= ttk.Entry(self.mainFrame, width=30,textvariable=self.dirPathText)
    self.dirPath.focus()
    self.dirPath.grid(column=1, row=0)
    self.fileExploreButton = ttk.Button(self.mainFrame,text="...",width=3,command = lambda:self.selectDir())    
    self.fileExploreButton.grid(column=2,row=0)

    #FilenameEntry
    ttk.Label(self.mainFrame, text='* Filename:',anchor='w').grid(column=0, row=1,sticky='w') 
    self.replacementText= tk.StringVar()
    self.replacement = ttk.Entry(self.mainFrame, width=30,textvariable=self.replacementText)
    self.replacement.grid(column=1, row=1)

    #FilenameEntry
    ttk.Label(self.mainFrame, text='Description:',anchor='w').grid(column=0, row=2,sticky='w') 
    self.descriptionText = tk.StringVar()
    self.description= ttk.Entry(self.mainFrame, width=30,textvariable=self.descriptionText)
    self.description.grid(column=1, row=2)

    self.mainFrame.grid(column=0, row=0)


    ##Button Frame 
    self.buttonFrame = ttk.Frame(root)
    self.buttonFrame.columnconfigure(0, weight=1)

    self.buttonStart = ttk.Button(self.buttonFrame, text='Start',command=lambda:self.startCaptureProcess(),cursor="hand2").grid(column=0, row=0)
    self.buttonTestData = ttk.Button(self.buttonFrame, text='Test Data',command=lambda:self.openTestDataWindow() ,cursor="hand2").grid(column=0, row=1)
    self.buttonOpenDirStyle = ttk.Style()
    self.buttonOpenDir = ttk.Button(self.buttonFrame, text='Open Dir',cursor="hand2",command=lambda:self.openWorkingDirectory()).grid(column=0, row=2)
    self.buttonGenerate = ttk.Button(self.buttonFrame, text='Generate',cursor="hand2",command=lambda:self.generateEvidence()).grid(column=0, row=3)

    for widget in self.buttonFrame.winfo_children():
      widget.grid(padx=3, pady=3)

    self.buttonFrame.grid(column=1, row=0)


  def openTestDataWindow(self):
    td = testDataWindow(self.root)

  def selectDir(self):
    dirSelected = fd.askdirectory()
    self.dirPathText.set(dirSelected) 


  def startCaptureProcess(self):
    if self.validInputData():
      self.setTestExecutionData()
      testData = self.getMetadata()
      self.evidence = Evidence(self.dirPathText.get(),self.replacementText.get(),testData,self.descriptionText.get())
      cap = captureWindow(self.root,self.evidence,self.dirPathText,self.replacementText,self.descriptionText) 
      if cap != None:
        self.weStart = True
    else:
      boxmessage.showerror("Input Data","The filename or Directory is not valid to store the evidence")

  def setTestExecutionData(self):
    status = self.setStatusTest()
    try:
      with open(jsonFilepath,'r') as f :
        config = json.load(f)
        config['Status'] = status
        config['TestCase'] = self.replacementText.get()
      with open(jsonFilepath,'w') as fi:
        json.dump(config,fi,indent=4)
    except FileNotFoundError as e:
      config = {}
      boxmessage.showerror(e)
    filename = self.replacementText.get()
    # filename_Status = "["+status+"] "+filename
    self.replacementText.set(filename)

  def validInputData(self):
    if not self.dirPathText.get().isspace() and self.dirPathText.get() != '' :
      if os.path.exists(self.dirPath.get()):
        if not self.replacementText.get().isspace() and self.replacementText.get() != '':
          return True
    return False

  def getMetadata(self):
    metadata = []
    try:
      with open(jsonFilepath,'r') as f:
        config = json.load(f)
        for key in config:
          metadata.append(config[key])
    except FileNotFoundError as e:
      config = {}
      boxmessage.showerror("Error",e)

    return metadata
  
  def setStatusTest(self):
    result = messagebox.askquestion("Test Status","¿The test case had passed?")
    if result == "yes":
      return "PASSED" 
    else:
      return "FAILED"
    
  def generateEvidence(self):
    if self.weStart:
      result = messagebox.askquestion("Generate Doc","¿You are sure to generate the document?")
      if result == "yes":
        self.evidence.closeDocument()
        messagebox.showinfo("Generate Doc","Document as been created successfuylly")
        self.openWorkingDirectory()
    else:
      boxmessage.showerror("We don´t start","First you must click Start button to capture the evidences")


  def openWorkingDirectory(self):
    subprocess.run(["explorer",os.path.realpath(self.dirPathText.get())])