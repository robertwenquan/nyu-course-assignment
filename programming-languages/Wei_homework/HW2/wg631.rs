use std::io;
use std::io::prelude::*;

fn check_all_digit(b:String)->i32 //return 1 if b is num
{
 let a = b.to_string();
 let mut result=1;
 if a.len()==0
 {
    result=0;
 }
 else
 {
   for x in a.chars()
   {
     if x.is_numeric()==false
     {
      result=0;
      break;
     }
   }
 } 
 result
}

fn get_name(b:String)->Vec<String>
{
    let mut p_flag=0;
    let mut name_vec=vec![];
    let a = b.to_string();
    let mut tmp_name="".to_string();

    for l in a.chars()
    {
        
        if l.to_string()=="{"
        {
           p_flag=1;
           continue;
        }

        if l.to_string()==":"
        {
            p_flag=0;
            let name=tmp_name.to_string();
            name_vec.push(name);
            tmp_name="".to_string();
            continue;
        }

        if p_flag==1
        {
            let tmp=&l.to_string();
            tmp_name.push_str(tmp);
        }
    }
    name_vec
}

fn get_item(b:String)->Vec<String>
{
    let mut p_flag=0;
    let mut name_vec=vec![];
    let a = b.to_string();
    let mut tmp_name="".to_string();

    for l in a.chars()//add item between : and ,
    {   
        if l.to_string()=="@" || l.to_string()=="{" ||l.to_string()=="}"
        {
          p_flag=0;
          tmp_name="".to_string();
        }    
        if l.to_string()==":"
        {
           p_flag=1;
           continue;
        }
        if l.to_string()==","
        {
            if p_flag==1
            {
            p_flag=0;
            let name=tmp_name.to_string();
            if check_all_digit(name.to_string())==0
            {
            name_vec.push(name);
            }
            tmp_name="".to_string();
            continue;
            }
        }
        if p_flag==1
        {
            let tmp=&l.to_string();
            tmp_name.push_str(tmp);
        }
    }  

    tmp_name="".to_string();
    p_flag=0;

    for l in a.chars()//add item between : and } 
    {  
        if l.to_string()=="@" || l.to_string()=="{" ||l.to_string()==","
        {
          p_flag=0;
          tmp_name="".to_string();
        }      

        if l.to_string()==":"
        {
           p_flag=1;
           continue;
        }
        if l.to_string()=="}"
        {
            if p_flag==1
            {
            p_flag=0;
            let name=tmp_name.to_string();
            
            if check_all_digit(name.to_string())==0
            {
            name_vec.push(name);
            }
            tmp_name="".to_string();
            continue;
            }
        }
        if p_flag==1
        {
            let tmp=&l.to_string();
            tmp_name.push_str(tmp);
        }
    }  

    tmp_name="".to_string();
    p_flag=0;

    for l in a.chars()//add item between , and }
    {   
        if l.to_string()=="@" || l.to_string()=="{" 
        {
          p_flag=0;
          tmp_name="".to_string();
        }  
        if l.to_string()==","
        {
           p_flag=1;
           continue;
        }
        if l.to_string()=="}"
        {
            if p_flag==1
            {
            p_flag=0;
            let name=tmp_name.to_string();

            if check_all_digit(name.to_string())==0
            {
            name_vec.push(name);
            }
            tmp_name="".to_string();
            continue;
            }
        }
        if p_flag==1
        {
            let tmp=&l.to_string();
            tmp_name.push_str(tmp);
        }
    }    

    tmp_name="".to_string();
    p_flag=0;

    for l in a.chars() //add item between , and ,
    {     
        if l.to_string()=="@" || l.to_string()=="{" ||l.to_string()=="}"
        {
          p_flag=0;
          tmp_name="".to_string();
        }
        if l.to_string()=="," && p_flag==0
        {
           p_flag=1;
           continue;
        }
        else if l.to_string()=="," && p_flag==1
        {
            let name=tmp_name.to_string();
            //println!("{}",tmp_name);
            if check_all_digit(name.to_string())==0
            {
            name_vec.push(name);
            }
            tmp_name="".to_string();
            continue;
        }
        if p_flag==1
        {
            let tmp=&l.to_string();
            tmp_name.push_str(tmp);
        }
    }     
    name_vec
}

fn get_ptr(b:String)->Vec<String>
{
    let mut p_flag=0;
    let mut name_vec=vec![];
    let a = b.to_string();
    let mut tmp_name="".to_string();

    for l in a.chars()
    {
        
        if l.to_string()=="@"
        {
           p_flag=1;
           continue;
        }

        if (l.to_string()=="," || l.to_string()=="}")&&(p_flag==1)
        {
            p_flag=0;
            let name=tmp_name.to_string();
            name_vec.push(name);
            tmp_name="".to_string();
            continue;
        }

        if p_flag==1
        {
            let tmp=&l.to_string();
            tmp_name.push_str(tmp);
        }
    }
    
    name_vec
}

fn check_legal(b:String)->i32 //return 0 if illegal
{

    let mut result=1;
    let mut left_cnt=0;
    let mut right_cnt=0;
    let mut mid_cnt=0;
    let a=b.to_string();
     for x in a.chars()
     {
        if x.to_string()=="{"
        {
            left_cnt=left_cnt+1;
        }
        if x.to_string()=="}"
        {
            right_cnt=right_cnt+1;
        }
        if x.to_string()==":"
        {
            mid_cnt=mid_cnt+1;
        }
     }
    
    let mut all_vec=vec![];
    let a = b.to_string();
    
    let tmp_vec1=get_name(a.to_string());
    let tmp_vec2=get_ptr(a.to_string());
    let tmp_vec3=get_item(a.to_string());
  
    for x in tmp_vec1
    {
        all_vec.push(x.to_string());
    }
    for x in tmp_vec2
    {
        all_vec.push(x.to_string());
    }
    for x in tmp_vec3
    {
        all_vec.push(x.to_string());
    }

    let mut first_flag:i32 =1;

    for x in all_vec
    {
        //println!("name,ptr,item {}",x);
        if x.len()==0
        {
          result=0;
          break;
        }
        for y in x.to_string().chars()
        {
            if first_flag==1
            {
              first_flag=0;
              if y.is_alphabetic()==false
              {
                result=0;
                break;
              }
            }
            else
            {
                if y.is_alphabetic()==true
                    {continue;}

                if y.is_numeric()==true
                    {continue;}
                else
                    {
                        result=0;
                        break
                    }
            }
        }
        first_flag=1;
    }

     if left_cnt==0
     {
       result=0;
     }

     if left_cnt!=right_cnt
     {
        result=0;
     }
     
     if mid_cnt!=left_cnt
     {
        result=0;
     }
     result
}

fn cal_sum(b:String)
{
    let mut a = b.to_string();//split(",");
    a=a.replace("{","");
    a=a.replace("}","");
    a=a.replace(":",",");
    let tmp_s=&a;
    let s_splited=tmp_s.split(",");
    let mut sum_result:i32=0;

    for x in s_splited
    {
        let num:i32 = x.parse().ok().unwrap_or_default();
        sum_result=sum_result+num;

    }

    println!("{}",sum_result);
}

fn name_check(b:String)
{
    let mut name_vec=vec![];
    let a = b.to_string();

    let tmp_vec1=get_name(a.to_string());
    for x in tmp_vec1
    {
        name_vec.push(x.to_string());
    }
    name_vec.sort();

    let mut first_flag=0;
    let vec_len=name_vec.len();

    for x in 0..vec_len-1
    {
        if x==0
        {
            if name_vec[x]==name_vec[x+1]
            {
                if first_flag==0
                {
                    first_flag=1;
                }
                else
                {
                    print!(",");
                }
                print!("{}",name_vec[x].to_string());
            }
        }
        else
        {
             
            if name_vec[x]!=name_vec[x-1]
            {
                if name_vec[x]==name_vec[x+1]
                {
                  if first_flag==0
                  {
                   first_flag=1;
                  }
                  else
                  {
                   print!(",");
                  }
                  print!("{}",name_vec[x].to_string());
                }
            }
        }
    }
    if first_flag==1
    {
      println!("");
    }
    else
    {
      println!("OK");
    }
}

fn ptr(b:String)
{
    let mut name_vec=vec![];
    let mut ptr_vec=vec![];
    let a = b.to_string();

    let tmp_vec1=get_name(a.to_string());
    for x in tmp_vec1
    {
        name_vec.push(x.to_string());
    }

    let tmp_vec2=get_ptr(a.to_string());
    for x in tmp_vec2
    {
        ptr_vec.push(x.to_string());
    }

    ptr_vec.sort();
    name_vec.sort();

    let name_vec_len=name_vec.len();

    let mut ptr_output_flag=0;
    for x in ptr_vec
    {
        let mut ptr_cnt=0;
        for y in 0..name_vec_len
        {
            if x==name_vec[y]
            {
              ptr_cnt=1;
            }
        }
        if ptr_cnt==0
        {
            if ptr_output_flag==0
            {
                print!("{}",x);
                ptr_output_flag=1;
            }
            else
            {
                print!(",{}",x);
            }
        }
        
    }

    if ptr_output_flag==0
    {
        println!("OK");
    }
    else
    {
        println!("");
    }
    
}

fn search(b:String,target:String,comma_flag:i32)->i32
{
        let mut name_vec=vec![];

        let tmp_vec1=get_name(b.to_string());
        for x in tmp_vec1
        {
            name_vec.push(x.to_string());
        }

        let c = b.to_string().replace(":",",");
        let d = c.to_string().replace("}",",");

        let c_split=d.split(",");
        let mut name_cnt=0;
        let mut result_vec:Vec<String>=vec![];

        let mut search_succ=0;
        for x in c_split
        {
            //println!("{}",x);
            if x.len()==0
            {
                result_vec.pop();
                continue;
            }
            if x==target
            {
                if comma_flag>0
                {
                print!(",");
                }
                else
                {
                  if search_succ==1
                  {
                  print!(",");
                  }
                
                }
                search_succ=1;
                
                let mut search_output_flag=0;

                let vec_len=result_vec.len();
           
                for x in 0..vec_len
                {
                 if search_output_flag==0
                  {
                    search_output_flag=1;
                  }
                  else
                  {
                    print!(":");
                  }
                  print!("{}",result_vec[vec_len-x-1].to_string());
                }
            }
            else
            {
                let name_char: Vec<char>=x.to_string().chars().collect();
                if name_char[0].to_string()=="{".to_string()
                {
                    result_vec.push(name_vec[name_cnt].to_string());
                    name_cnt=name_cnt+1;
                }
            }
        }
        
        search_succ    
}

fn main(){

    let mut period_flag=0;
    let mut quit_flag=0;

    let mut data_lines = vec![];
    let mut comm_lines = vec![];
    let mut sum_input="".to_string();
    let mut namecheck_input="".to_string();
    let mut ptr_input="".to_string();
    
    let stdin = io::stdin();
    for line in stdin.lock().lines(){
        let mut current_input = line.unwrap();
        current_input=current_input.replace(" ","");
            if current_input == "QUIT"
            {
                quit_flag=1;
                break;
            }
            if current_input == "."
            {
                period_flag=1;
                continue;
            }
            if period_flag==0
            {
                data_lines.push(current_input);   
            }
            else
            {
                comm_lines.push(current_input);
            }
    }

    let check_flag=period_flag+quit_flag;

    let mut data_legal=0;
    for x in data_lines.iter()
    {
        let tmp_check_result=check_legal(x.to_string());
        if tmp_check_result==0 //illegal
        {
            data_legal=data_legal+1;
            break;
        }

    }

    let mut comm_legal=0;
    for y in comm_lines.iter()
    {
        if str::eq(y,"SUM")
            {continue;}
        if str::eq(y,"sum")
            {continue;}
        if str::eq(y,"NAMECHECK")
            {continue;}
        if str::eq(y,"namecheck")
            {continue;}
        if str::eq(y,"PTRS")
            {continue;}
        if str::eq(y,"ptrs")
            {continue;}

        let mut tmp_comm=y.to_string();
        if tmp_comm.len()>6
        {
              tmp_comm.truncate(6);
              if (str::eq(&tmp_comm,"SEARCH")) || (str::eq(&tmp_comm,"search"))
                {continue;}
              else
              {
                comm_legal=comm_legal+1;
                break;
              }
        }
        else
        {
            comm_legal=comm_legal+1;
            break;
        }      
    }
    if (check_flag<2) || (data_legal!=0) || (comm_legal!=0)
    {
        println!("ERR");
    }
    else
    {
        for comm in comm_lines.iter()
        {
            if (str::eq(comm,"SUM"))|| (str::eq(comm,"sum"))
            {
                 for x in data_lines.iter()
                  {
                    let x_tmp = &x ;
                    sum_input.push_str(x_tmp);
                    sum_input.push_str(",");
                  }
                   cal_sum(sum_input.to_string());
            }

            else if (str::eq(comm,"NAMECHECK")) || (str::eq(comm,"namecheck"))
            {
                 for x in data_lines.iter()
                  {
                    let x_tmp = &x ;
                    namecheck_input.push_str(x_tmp);
                    namecheck_input.push_str(",");
                  }
                   name_check(namecheck_input.to_string());
            }

            else if (str::eq(comm,"PTRS")) || (str::eq(comm,"ptrs"))
            {
                 for x in data_lines.iter()
                  {
                    let x_tmp = &x ;
                    ptr_input.push_str(x_tmp);
                    ptr_input.push_str(",");
                  }
                   ptr(ptr_input.to_string());
            }

            else 
            {
                 let mut tmp_comm=comm.to_string();
                 if tmp_comm.len()>6
                 {
                    tmp_comm.truncate(6);
                    if (str::eq(&tmp_comm,"SEARCH"))||(str::eq(&tmp_comm,"search"))
                    {
                     let d=comm.to_string();
                     let mut d_split = d.replace("SEARCH","");
                     d_split = d_split.replace("search","");
                     let mut found_flag=0;

                      for x in data_lines.iter()
                      {
                       let tmp_found_flag=search(x.to_string(),d_split.to_string(),found_flag);
                       if tmp_found_flag==1
                        {
                        found_flag=found_flag+1;
                        }
                      }  

                      if found_flag==0
                      {
                       println!("NIL");
                      }
                      else
                      {
                       println!("");
                      }
                    }
                 }

            }
       }
    }

}

