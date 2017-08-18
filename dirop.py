import os
import sys

def GetFileList(dirpath):
	assert os.path.isdir(dirpath),"dir {} doesn't exist".format(dirpath)
	filelist=[]
	files=os.listdir(dirpath)
	for f in files:
		full_path=os.path.join(dirpath,f)
		if os.path.isfile(full_path):
			filelist.append(f)
	return filelist
def GetDirList(dirpath):
	assert os.path.isdir(dirpath),"dir {} doesn't exist".format(dirpath)
	dirlist=[]
	files=os.listdir(dirpath)
	for f in files:
		full_path=os.path.join(dirpath,f)
		if os.path.isdir(full_path):
			dirlist.append(f)
	return dirlist
def GetFullPathFileList(dirpath):
	assert os.path.isdir(dirpath),"dir {} doesn't exist".format(dirpath)
	filelist=[]
	files=os.listdir(dirpath)
	for f in files:
		full_path=os.path.join(dirpath,f)
		if os.path.isfile(full_path):
			filelist.append(full_path)
	return filelist
def GetFullPathDirList(dirpath):
	assert os.path.isdir(dirpath),"dir {} doesn't exist".format(dirpath)
	dirlist=[]
	files=os.listdir(dirpath)
	for f in files:
		full_path=os.path.join(dirpath,f)
		if os.path.isdir(full_path):
			dirlist.append(full_path)
	return dirlist

def GetFormatFileList(dirpath,formatlist):
	assert os.path.isdir(dirpath),"dir {} doesn't exist".format(dirpath)
	files=GetFileList(dirpath)
	newlist=[]
	for f in files:
		for ft in formatlist:
			if f.endswith(ft):
				newlist.append(f)
				break
	return newlist
def GetFullPathFormatFileList(dirpath,formatlist):
	assert os.path.isdir(dirpath),"dir {} doesn't exist".format(dirpath)
	files=GetFileList(dirpath)
	newlist=[]
	for f in files:
		for ft in formatlist:
			full_path=os.path.join(dirpath,f)
			if os.path.isfile(full_path) and f.endswith(ft):
				newlist.append(full_path)
				break
	return newlist
def FullPath2Short(fullpath):
	return fullpath.split('/')[-1]
def RenameFiles(dirpath,prefix=None,width=5,im_format=[".jpg"]):
	ims=GetFullPathFormatFileList(dirpath,im_format)
	if prefix==None:
		prefix=dirpath.split("/")[-1]
	index=0
	for im in ims:
		suffix=im.split('.')[-1]
		newname="{}_{}.{}".format(prefix,str(index).zfill(5),suffix)
		os.rename(im,os.path.join(dirpath,newname))
		print("renamed {} to {} successfully!!".format(im,newname))
		index+=1
def RenamebyList(dirpath,listfile):
	namedict={}
	with open(listfile,"r") as f:
		namelists=f.readlines()
	for line in namelists:
		pair=line.replace('\n','').split()
		if len(pair)>=2:
			namedict[pair[0]]=pair[1]
	fs=os.listdir(dirpath)
	for f in fs:
		newname=namedict.get(f,"")
		if newname!="":
			os.rename(os.path.join(dirpath,f),os.path.join(dirpath,newname))
			print("renamed {} to {} successfully!!".format(f,newname))

class DirTree:
	def __init__(self):
		self.layer_number=0
		self.root_dir=""
		self.root_tree={}
		self.all_keys=[]
	def Clear(self):
		self.layer_number=0
		self.root_tree={}
		self.all_keys=[]
	def Update(self):
		self.Clear()
		self.LoadFromRoot(self.root_dir)
	def LoadFromRoot(self,rootdir):
		#------------------------------
		#instruct the file tree layerwise
		#root_tree-->{rootdir:{subdir1:{...},subdir2:{...}}		
		#------------------------------
		self.Clear()
		
		self.root_dir=rootdir
		self.root_tree[rootdir]={}
		self.all_keys=[rootdir]
		
		parents=[self.root_tree]
		nextparents=[]
		next_dirs=[]

		bfinished=False
		while not bfinished:
			nextparents=[]
			bfinished=True
			self.layer_number+=1
			for  p in parents:
				for sub_dir in p.keys():
					subsub_dirs=GetFullPathDirList(sub_dir)
					self.all_keys.extend(subsub_dirs)
					if len(subsub_dirs)>0:
						bfinished=False
					for dirs in subsub_dirs:
						p[sub_dir][dirs]={}
					nextparents.append(p[sub_dir])	
			parents=nextparents[:]
			
	def GetSubDirs(self,curdir):
		key=curdir
		assert key in self.all_keys,"key error!unkown key {}.".format(key)
		parents=[self.root_tree]
		nextparents=[]
		next_dirs=[]

		bfinished=False
		while not bfinished:
			nextparents=[]
			bfinished=True
			for p in parents:
				if len(p.keys())>0:
					bfinished=False
				if key in p.keys():
					return p[key].keys()
				for pkey in p.keys():
					nextparents.append(p[pkey])
			parents=nextparents[:]
	def GetLayerDirs(self,layer_number):
		assert layer_number==-1 or layer_number>0,"layer number must be >0 or =-1,(request layer_number:{})".format(layer_number)
		assert layer_number<=self.layer_number,"layer number exceeded,({} vs {}).".format(layer_number,self.layer_number)
		parents=[self.root_tree]
		nextparents=[]
		layer_keys=[]
		next_dirs=[]
		cur_number=0

		bfinished=False
		while not bfinished:
			cur_number+=1
			nextparents=[]
			last_layer_keys=layer_keys[:]
			layer_keys=[]
			bfinished=True
			for p in parents:
				if len(p.keys())>0:
					bfinished=False
				for pkey in p.keys():
					nextparents.append(p[pkey])
					layer_keys.append(pkey)
			parents=nextparents[:]
			if cur_number==layer_number:
				return layer_keys
			if bfinished and layer_number==-1:
				return last_layer_keys
	def Display(self):
		parents=[self.root_tree]
		bfinished=False
		while not bfinished:
			nextparents=[]
			bfinished=True
			for p in parents:
				if len(p.keys())>0:
					bfinished=False
				for key in p.keys():
					print "==============="
					print "parent_dir: {}:".format(key)
					print "--------------"
					print "sub_dirs:"
					for subkey in p[key].keys():
						print subkey 
				for key in p.keys():
					nextparents.append(p[key])
			parents=nextparents[:]
				
if __name__=="__main__":
	root_dir=sys.argv[1]
	ft=DirTree()
	ft.LoadFromRoot(root_dir)
	ft.Display()
	print ft.GetLayerDirs(-1)[0]

