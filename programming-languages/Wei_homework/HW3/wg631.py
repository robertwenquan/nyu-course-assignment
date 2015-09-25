

global type_dict
type_dict=dict()
global tmp_var
tmp_var=[]
global err_flag
err_flag=0
global bottom_flag
bottom_flag=0

def is_var(var_name):
    if len(var_name)==0:
        return False
    if var_name[0]!='`':
        return False
    x=var_name[1:]
    tmp_len=len(x)
    if tmp_len==0:
        return False
    else:
        if tmp_len==1:
            return x.isalpha()
        else:
            if x[0].isalpha()==False:
                return False
            else:
                for i in x[1:]:
                    if i.isdigit()==False and i.isalpha()==False:
                        return False
            return True
        
def is_pri(x):
    return (x in ["str","int","real"])

def is_arglist(x):
    if x=="()":
        return True
    tmp_len=len(x)
    if tmp_len<2:
        return False
    if x[0]!='(' or x[tmp_len-1]!=')':
        return False
    tmp_x=x[1:tmp_len-1]
    tmp_x_list=tmp_x.split(',')
    for item in tmp_x_list:
        if check_type(item)==4:
            return False
    return True

def split_arg(input_list):
    result=[]
    x=input_list[1:-1]
    if x=="":
        return result
    find_start_index=0
    while 1:
        tmp_index=x.find(',',find_start_index)
        if tmp_index!=-1:
            tmp_data=x[:tmp_index]
            if check_type(tmp_data)!=4:
                result.append(tmp_data)
                x=x[tmp_index+1:]
                find_start_index=0
            else:
                find_start_index=tmp_index+1
                if find_start_index>len(x)-1:
                    break
                else:
                    continue
        else:
            result.append(x)
            break
    return result  
        
def is_func(func_name):
    tmp_len=len(func_name)
    if tmp_len<=2:
        return False
    if "->" not in func_name:
        return False
    flag_index=func_name.rindex("->")
    l_p=func_name[:flag_index]
    if flag_index+2>tmp_len-1:
        return False
    r_p=func_name[flag_index+2:]
    if is_arglist(l_p)==False:
        return False
    if check_type(r_p)==4:
        return False
    return True
    
    
def is_list(list_name):
    tmp_len=len(list_name)
    if tmp_len<=2:
        return False
    else:
        x=list_name[1:-1]
        if is_pri(x) or is_var(x):
            return True
        return False
       
#0 var,1 pri,2 func,3 list,4 err
def check_type(x): 
    if is_pri(x):
        return 1
    
    if is_func(x):
        return 2
    
    if is_var(x):
        return 0
    
    if is_list(x):
        return 3
    
    return 4

def has_one_flag(x):
    cnt=0
    for i in x:
        if i == '^':
            cnt+=1
    return True if cnt==1 else False

def check_var(s):
    if s[0].isalpha()==False:
            return False
    else:
        for i in range(1,len(s),1):
            if s[i].isalpha() == False and s[i].isdigit()==False:
                    return False
        return True
        
def check_one_space(s):
    s=s.replace('(',' ')
    s=s.replace(')',' ')
    s=s.lstrip().rstrip()
    for x in s:
        if x==' ':
            return False
    s_len=len(s)
    if s_len<2:
        return False
    else:
      if s[0]=='`':
        return check_var(s[1:])
      else:
        return (s in ["int","real","str"])


def check_space(s):
    s=s.replace('^',',')
    s=s.replace('->',',')
    s=s.replace('[',' ')
    s=s.replace(']',' ')
    split_result=s.split(',')
    tmp_data=[]
    for x in split_result:
        if x.replace(" ", "")!="()":
            tmp_data.append(x)
    for x in tmp_data:
        if check_one_space(x)==False:
            return False
    return True
  
def check_legal(x):
    if has_one_flag(x)==False or check_space(x)==False:
        return False
    x = x.replace(" ","")
    left_p,right_p=x.split('^')[0],x.split('^')[1]
    if check_type(left_p)==4 or check_type(right_p)==4:
        return False
    return True

class my_parse_tree:
    def __init__(self,x):
        self.child_list=[]
        self.return_type=None
        self.value=None
        self.my_type=None
        self.forward_link=None
         
        if x=="":
            self.my_type=1
            self.value=''
            
        if check_type(x)==1:
            self.my_type=1
            self.value=x
        
        elif check_type(x)==0:
            self.my_type=0
            self.value=x
        
        elif check_type(x)==3:
            self.my_type=3
            self.value=my_parse_tree(x[1:-1])
        
        else:
            self.my_type=2
            flag_index=x.rindex("->")
            self.l_p=x[:flag_index] 
            self.r_p=x[flag_index+2:]
            tmp_data=split_arg(self.l_p)
            for item in tmp_data:
                self.child_list.append(my_parse_tree(item))
            self.return_type=my_parse_tree(self.r_p)
            
    def tree_print(self):
        if self.my_type==1 or self.my_type==0:
            print(self.value,end="")
            
        if self.my_type==3:
            print('[',end="")
            self.value.tree_print()
            print(']',end="")
            
        if self.my_type==2:
            print('(',end='')
            tmp_len=len(self.child_list)
            if tmp_len>0:
                for i in range(tmp_len-1):
                    self.child_list[i].tree_print()
                    print(',',end='')
                self.child_list[tmp_len-1].tree_print()
            print(')->',end='')
            self.return_type.tree_print()
    
    def tree_print_unify(self):
        if self.my_type==1:
            print(self.value,end="")
        
        if self.my_type==0:
            if self.value in type_dict:
                print(type_dict[self.value],end="")
            else:
                print(self.value,end="")
            
        if self.my_type==3:
            print('[',end="")
            self.value.tree_print()
            print(']',end="")
            
        if self.my_type==2:
            print('(',end='')
            tmp_len=len(self.child_list)
            if tmp_len>0:
                for i in range(tmp_len-1):
                    self.child_list[i].tree_print_unify()
                    print(',',end='')
                self.child_list[tmp_len-1].tree_print_unify()
            print(')->',end='')
            self.return_type.tree_print_unify()

def check_recurisve():
    global bottom_flag
    for x in type_dict:
        if type_dict[x]==x:
            bottom_flag=1
            
def my_parse(x):
    x = x.replace(" ","")
    left_p,right_p=x.split('^')[0],x.split('^')[1]  
    left_tree=my_parse_tree(left_p)
    right_tree=my_parse_tree(right_p)
    unify_tree(left_tree, right_tree)
    dict_revised()
    check_recurisve()
    if bottom_flag==1:
        print('BOTTOM',end="")
    else:
        left_tree.tree_print_unify()
    
def check_bottom(a,b):
    global bottom_flag
    
    if a.my_type==2 and b.my_type==2:
        if len(a.child_list)!=len(b.child_list):
            bottom_flag=1
            
    if a.my_type==1:
        if b.my_type==1:
            if b.value!=a.value:
                bottom_flag=1 
        else:
            if b.my_type==2 or b.my_type==3:
                bottom_flag=1
    
    if a.my_type==0:
        if a.value in type_dict:
            tmp_tree=my_parse_tree(type_dict[a.value])
            check_bottom(tmp_tree, b)
            check_bottom(b, tmp_tree)
          
def unify_tree(a,b):
    check_bottom(a, b)
    check_bottom(b, a)
    if bottom_flag!=1:
      if a.my_type==0 :
        if b.my_type!=3:
          if a.value!=b.value:        
             type_dict[a.value]=b.value
        else:
          type_dict[a.value]='['+b.value.value+']'
      elif b.my_type==0:
        if a.my_type!=3:
          if a.value!=b.value:
             type_dict[b.value]=a.value
        else:
          type_dict[b.value]='['+a.value.value+']'
      else:
        tmp_len=len(a.child_list)
        for i in range(tmp_len):
            unify_tree(a.child_list[i], b.child_list[i])
        if a.return_type!=None:
            unify_tree(a.return_type, b.return_type)

def revise_item(x,y):
        if is_pri(y):
            pass
        elif is_var(y):
            if y in tmp_var:
                err_flag=1
                return False
            else:
                tmp_var.append(x)
                if y in type_dict:
                   revise_item(y, type_dict[y])
                   type_dict[x]=type_dict[y]
                tmp_var.pop()
        elif is_list(y):
            y_tmp=y[1:-1]
            if y_tmp in type_dict:
                revise_item(y_tmp, type_dict[y_tmp])
                type_dict[x]='['+type_dict[y_tmp]+']'
            else:
                pass
            
        else:
            pass
        
        return True
        
def dict_revised():
    for x in type_dict:
        y=type_dict[x]
        revise_item(x,y)
    
if __name__ == "__main__":
   while(1): 
     try:
        x=input()
        if x == "QUIT":
          break
        if check_legal(x):
           my_parse(x)
           print()
           if bottom_flag==1:
              break
        else:
          print("ERR")
          break
     except EOFError:
        print("ERR")
        break

              
