from CssCore.init import *
# from init import *

class VerifyData:
    def __init__(self, VerifyDataAddress):
        self.FileFullName = os.path.split(VerifyDataAddress)[1]
        self.FileName = self.FileFullName.split('.')[0]
        self.UserDataDir = os.path.join(USER_DATA_DIR, self.FileName)
        if (os.path.isdir(self.UserDataDir) == False):
            raise ValueError("file {} is not a dir.".format(self.UserDataDir))
        else:
            BackUpDir = os.getcwd()
            os.chdir(self.UserDataDir)

            FileToRead = open("%s.pickle"%(self.FileName), "rb")
            self.MerkleTree = pickle.load(FileToRead)
            FileToRead.close()

            with open('%s.json'%(self.FileName), 'r') as fp_read:
                Metadata = json.load(fp_read)
                self.Metadata = {"NumberOfShard": Metadata["NumberOfShard"], 
                                "SizeOfShard": Metadata["SizeOfShard"],
                                "RootHash": Metadata["RootHash"],
                                "PublicLeafHash": Metadata["PublicLeafHash"]}
            fp_read.close()
            
            for i in range(0, self.Metadata["NumberOfShard"]):
                if os.path.isfile("%s_shard%d.txt"%(self.FileName, i)):
                    os.remove("%s_shard%d.txt"%(self.FileName, i))

            FileIn = open(self.FileFullName, "rb")
            ChunkIndex = 0
            while True:
                Chunk = FileIn.read(self.Metadata["SizeOfShard"])
                if Chunk:
                    FileOut = open("%s_shard%d.txt"%(self.FileName, ChunkIndex), "wb")
                    FileOut.write(Chunk)
                    FileOut.close()
                    ChunkIndex += 1
                else: 
                    break

            os.chdir(BackUpDir)

    def GenerateAuxiPath(self, ShardIndex):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir) 

        fp = open("%s_shard%d.txt"%(self.FileName, ShardIndex), 'rb')
        ShardData = str(fp.read())
        fp.close()
        os.chdir(BackUpDir)
        PriShardHash = self.MerkleTree.compute_hash(ShardData)
        PubShardHash = self.MerkleTree.compute_hash(PriShardHash)

        AuxiPath = False
        for index, leaf in enumerate(self.MerkleTree.leaves):
            if index == ShardIndex:
                AuxiPath = self.MerkleTree.generateMerklePath(leaf)

        if (AuxiPath != False):
            return PubShardHash, AuxiPath
        else:
            return False

    def GenerateOutputForBc(self, ShardIndex):
        # True = is left child
        # False = is right child
        PubShardHash, AuxiPath = self.GenerateAuxiPath(ShardIndex)
        if (AuxiPath == False):
            return False
        OutputBc = []
        for i in range(0, len(AuxiPath)):
            if (i == 0):
                if (AuxiPath[i][1] == True): # Is Left Child
                    # Left - Right
                    element = (str(AuxiPath[i][0]), str(PubShardHash))
                else: # Is Right Child
                    # Left - Right
                    element = (str(PubShardHash), str(AuxiPath[i][0]))
            elif (i == len(AuxiPath)-1):
                continue
            else:
                if (AuxiPath[i][1] == True): # Is Left Child
                    # Left - Right
                    element = (str(AuxiPath[i][0]), 'NULL')
                else: # Is Right Child
                    # Left - Right
                    element = ('NULL', str(AuxiPath[i][0]))
            OutputBc.append(element)

        return OutputBc

    def SaveToJson(self, OutputBc):
        self.OuputBcDict = {"FileFullName": self.FileFullName, 
                            "NumberOfStep": len(OutputBc),
                            "UserEmail": "abc@hcmut.edu.vn",
                            "ContractAddress": "0x1234556"}

        AuxiPath = []
        for i in range(0, len(OutputBc)):
            AuxiPath.append({"Left":  OutputBc[i][0],
                                 "Right": OutputBc[i][1]})
        self.OuputBcDict["AuxiPath"] = AuxiPath

        # print(AuxiPath)
        return self.OuputBcDict
    
    def CleanUpData(self):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir)
        for i in range(0, self.Metadata["NumberOfShard"]):
            if os.path.isfile("%s_shard%d.txt"%(self.FileName, i)):
                os.remove("%s_shard%d.txt"%(self.FileName, i))
            else:
                print("Error: %s file not found" % "%s_shard%d.txt"%(self.FileName, i))
        os.chdir(BackUpDir)

    def CleanUpOutputResult(self):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir)
        if os.path.isfile('%s_OutputBc.json'%self.FileName):
            os.remove('%s_OutputBc.json'%self.FileName)
        else:    ## Show an error ##
            print("Error: %s file not found" % '%s_OutputBc.json'%self.FileName)
        os.chdir(BackUpDir)

def ReturnAuxiPath(VerifyDataAddress, VerifyDataShardId=None):
    Verify = VerifyData(VerifyDataAddress)
    if (VerifyDataShardId == None):
        VerifyDataShardId = random.randint(0, Verify.Metadata["NumberOfShard"])
    elif (VerifyDataShardId >= Verify.Metadata["NumberOfShard"]):
        print("ERROR!!! Using wrong shard ID \n")
        return False

    OutputBc = Verify.GenerateOutputForBc(VerifyDataShardId)
    Verify.CleanUpData()
    if (OutputBc != False):
        return Verify.SaveToJson(OutputBc)
    else:
        return False

# print(ReturnAuxiPath("/Users/khanhtran/2070102/DE/CSS/UserData/all_log/all_log.txt", 2))
