from CssCore.init import *

class UserProfile:  
    def __init__(self, InputFile):
        InputSplit = InputFile.split('/')
        self.FileFullName = str(InputSplit[len(InputSplit)-1])
        self.FileName = str(self.FileFullName.split('.')[0])
        self.UserDataDir = os.path.join(USER_DATA_DIR, self.FileName)

        MetadataFullName = str(self.FileName) + ".json"
        self.MetadataFullName = MetadataFullName
        # InputDir = str(os.path.split(InputFile)[0]) + '/'

        # InputMetadataDir = str(InputSplit[0:(len(InputSplit)-1)])
        InputMetadata = os.path.join(INPUT_DATA_DIR, MetadataFullName)
        InputFile = os.path.join(INPUT_DATA_DIR, self.FileFullName)

        print(InputFile)
        print(InputMetadata)
        try:
            data = open(InputFile, 'r')
            metadata = open(InputMetadata, 'r')
        except IOError:
            print("File not accessible")
            raise Exception()
        finally:
            data.close()
            metadata.close()

        try:
            os.mkdir(self.UserDataDir)
        except OSError as error:
            print(error)
            print("%s name had been used!!! Please used another name", self.FileFullName)
            raise Exception()

        copy(InputFile, self.UserDataDir)
        copy(InputMetadata, self.UserDataDir)
        self.UpdateMetadata()

    def UpdateMetadata(self):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir)

        with open('%s'%(self.MetadataFullName), 'r') as fp_read:
            Metadata = json.load(fp_read)
            self.Metadata = {"NumberOfShard": Metadata["NumberOfShard"], 
                             "SizeOfShard": Metadata["SizeOfShard"],
                             "RootHash": Metadata["RootHash"],
                             "PublicLeafHash": Metadata["PublicLeafHash"]}
        fp_read.close()
        os.chdir(BackUpDir)

    def VerifyPublicTree(self):
        self.MerkleTree = MerkleTree(is_external=True, ex_leaf=self.Metadata["PublicLeafHash"])
        if (self.MerkleTree.root.hash == self.Metadata["RootHash"]):
            return True
        else: 
            return False

    def VerifyDataShard(self):
        if (self.ShardingData() == self.Metadata["NumberOfShard"]):
            ShardIndex = random.randint(0, self.Metadata["NumberOfShard"])
            BackUpDir = os.getcwd()
            os.chdir(self.UserDataDir)
            fp = open("%s_shard%d.txt"%(self.FileName, ShardIndex), "rb")
            data = str(fp.read())
            fp.close()
            os.chdir(BackUpDir)
            FirstShardHash = self.MerkleTree.compute_hash(data)
            SecondShardHash = self.MerkleTree.compute_hash(FirstShardHash)
            if (SecondShardHash == self.Metadata["PublicLeafHash"][ShardIndex]):
                return True
            else:
                return False
        else:
            
            return False

    def ShardingData(self):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir)
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
        return ChunkIndex

    def StoreMekleTree(self):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir)
        FileToStore = open("%s.pickle"%(self.FileName), "wb")
        pickle.dump(self.MerkleTree, FileToStore)
        FileToStore.close()
        os.chdir(BackUpDir)  

    def CleanUpData(self):
        BackUpDir = os.getcwd()
        os.chdir(self.UserDataDir)
        for i in range(0, self.Metadata["NumberOfShard"]):
            if os.path.isfile("%s_shard%d.txt"%(self.FileName, i)):
                os.remove("%s_shard%d.txt"%(self.FileName, i))
            else:
                print("Error: %s file not found" % "%s_shard%d.txt"%(self.FileName, i))
        os.chdir(BackUpDir)

    def CleanUpWhenFailed(self): 
        print(self.UserDataDir)
        if os.path.isdir(self.UserDataDir):
            rmtree(self.UserDataDir)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(self.UserDataDir))

        # os.chdir(BackUpDir)

def PreprocessingData(FileName):
    InputFile = os.path.join(str(INPUT_DATA_DIR) + FileName)
    try:
        UserData = UserProfile(InputFile)
    except OSError:
        return 1

    VerifyPublicTree = UserData.VerifyPublicTree()
    VerifyDataShard = UserData.VerifyDataShard()
    # print(VerifyPublicTree)
    # print(VerifyDataShard)
    if (VerifyPublicTree == True & VerifyDataShard == True):
        UserData.StoreMekleTree()
    else:
        UserData.CleanUpWhenFailed()
        del UserData
        return 2

    UserData.CleanUpData()

    return UserData.UserDataDir + '/' + UserData.FileFullName

# try:
# print(PreprocessingData(str(INPUT_DATA_DIR) + "/all_log.txt"))
# except:
#     print("\n\n")

