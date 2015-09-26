#global input
$user_input=[]
$user_input_count=0

#define methods
#split string to arrays
def my_split(s)
  s_len=s.length
  split_result=[]
  tmp_i=0
  tmp_stack=''
  while tmp_i<s_len
   case s[tmp_i]
     when '+','-','*','/','(',')' 
       if tmp_stack.length>=0
         split_result.push(tmp_stack)
         tmp_stack=''
       end
       split_result.push(s[tmp_i])
     else
       tmp_stack+=s[tmp_i]
   end
   tmp_i+=1
 end
 
  if tmp_stack.length>0
    split_result.push(tmp_stack)
  end  
  split_result.delete_if{|x| x==''}
  return split_result
end

#check input
def check_input
  tmp_i=0
  flag=0
  while tmp_i+1 < $user_input_count do
    tmp_flag=check_one_line($user_input[tmp_i])
    tmp_i+=1
    if tmp_flag==1
      flag=1
      break
    end
  end
  if flag==1  #flag==1, illegal input, else legal input.
    return true
  else
    return false
  end
end

#check pairs of parenthesis
def check_one_line(s) 
  left_p_count=0
  right_p_count=0
  s_len=s.length
  tmp_index=0
  while tmp_index<s_len do
    if s[tmp_index]=='('
      left_p_count+=1
    elsif s[tmp_index]==')'
      right_p_count+=1
    end
    tmp_index+=1
  end
  if left_p_count!=right_p_count
    return 1
  else
    return 0
  end
end

def cal_without_p(s)
test=my_split(s)

a_cnt=0
b_cnt=0
c_cnt=0
d_cnt=0

test.each do |x|
  case x
    when '+'
      a_cnt+=1
    when '-'
      b_cnt+=1
    when '*'
      c_cnt+=1
    when '/'
      d_cnt+=1
  end
end
#puts a_cnt,b_cnt,c_cnt,d_cnt

tmp_i=0
while tmp_i<c_cnt do
  opt_index=test.index('*')
  tmp_value=test[opt_index-1].to_i*test[opt_index+1].to_i
  test[opt_index-1]=tmp_value.to_s
  test.delete_at(opt_index)
  test.delete_at(opt_index)
  tmp_i+=1
end

tmp_i=0
while tmp_i<d_cnt do
  opt_index=test.index('/')
  tmp_value=test[opt_index-1].to_i/test[opt_index+1].to_i
  test[opt_index-1]=tmp_value.to_s
  test.delete_at(opt_index)
  test.delete_at(opt_index)
  tmp_i+=1
end

tmp_i=0
while tmp_i<a_cnt+b_cnt do
  opt_index=test.index('+')
  opt_index_2=test.index('-')
  if opt_index==nil
  tmp_value=test[opt_index_2-1].to_i-test[opt_index_2+1].to_i
  test[opt_index_2-1]=tmp_value.to_s
  test.delete_at(opt_index_2)
  test.delete_at(opt_index_2)
  elsif opt_index_2==nil
  tmp_value=test[opt_index-1].to_i+test[opt_index+1].to_i
  test[opt_index-1]=tmp_value.to_s
  test.delete_at(opt_index)
  test.delete_at(opt_index)
  elsif opt_index<opt_index_2 
  tmp_value=test[opt_index-1].to_i+test[opt_index+1].to_i
  test[opt_index-1]=tmp_value.to_s
  test.delete_at(opt_index)
  test.delete_at(opt_index)
  else
  tmp_value=test[opt_index_2-1].to_i-test[opt_index_2+1].to_i
  test[opt_index_2-1]=tmp_value.to_s
  test.delete_at(opt_index_2)
  test.delete_at(opt_index_2)
  end
  tmp_i+=1
end

return test
end

def my_cal(tmp)
  l_p_cnt=0
  tmp=my_split(tmp)
  tmp.each do |x|
    if x=='('
      l_p_cnt+=1
    end
  end
  tmp_p_cnt=0
  while tmp_p_cnt<l_p_cnt do
    tmp_l_p=tmp.rindex('(')
    tmp_r_p=tmp.index(')')
    tmp_p_cnt+=1 
    tmp_cal_arr=tmp[tmp_l_p+1..tmp_r_p-1]
    tmp_cal_result=cal_without_p(tmp_cal_arr)
    tmp[tmp_l_p]=tmp_cal_result[0].to_s
    tmp.slice!(tmp_l_p+1..tmp_r_p)
  end
  if tmp.size>1
    tmp=cal_without_p(tmp)
  end
  puts tmp
end

def cal_input
  tmp_input_index=0
  while tmp_input_index<$user_input_count-1 do
    my_cal($user_input[tmp_input_index])
    tmp_input_index+=1
  end
end

#start main loop
loop do 
  break if STDIN.eof?
  $user_input_count+=1
  tmp_input=gets.chomp()
  tmp_input=tmp_input.gsub(' ','')
  $user_input.push(tmp_input)
  break if tmp_input=='QUIT'
end

if $user_input[$user_input_count-1]!='QUIT'
  puts 'ERR'
elsif check_input==true
  puts 'ERR'
else
  cal_input
end

