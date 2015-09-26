/* 
File Name: "fshader53.glsl":
           Fragment Shader
*/

// #version 150 


in  vec4 color;
in vec2 texCoord;
in vec2 lat_Coord;
in float fog_d;
in float fog_f;

in  float float_texture;

out vec4 fColor;
uniform sampler2D texture_2D;
uniform sampler1D texture_1D;
uniform int text_ground_flag;
uniform int f_sphere_flag;
uniform int f_sphere_check_flag;
uniform int enable_lat;
uniform int f_draw_shadow_lat;

void main() 
{  
vec4 tex_color=color;

if (text_ground_flag==1 && f_sphere_flag==0)
{
tex_color = color*texture(texture_2D,texCoord);
}

if (f_sphere_flag==1 && text_ground_flag==0 )
{
tex_color=color*texture(texture_1D,float_texture);
if(enable_lat>0)
{
float s=lat_Coord[0];
float t=lat_Coord[1];
if(fract(4*s)<0.35 && fract(4*s)>0 && fract(4*t)>0 && fract(4*t)<0.35) discard;
}
}

if(f_sphere_check_flag==1  && text_ground_flag==0)
{
vec4 tmp_color=texture(texture_2D,texCoord);
if(tmp_color[0]==0)
{tmp_color=vec4(0.9,0.1,0.1,1.0);}
tex_color=color*tmp_color;
if(enable_lat>0)
{
float s=lat_Coord[0];
float t=lat_Coord[1];
if(fract(4*s)<0.35 && fract(4*s)>0 && fract(4*t)>0 && fract(4*t)<0.35) discard;
}
}

if(f_draw_shadow_lat==1)
{
if(enable_lat>0)
{
float s=lat_Coord[0];
float t=lat_Coord[1];
if(fract(4*s)<0.35 && fract(4*s)>0 && fract(4*t)>0 && fract(4*t)<0.35) discard;
}
}
vec4 fog_color=vec4(0.7,0.7,0.7,0.5);

if(fog_f==1.0)
{ fColor =tex_color;}
else if(fog_f==2.0)
{ float x=clamp(fog_d,0.0,18.0); fColor=mix(tex_color,fog_color,x/18);}
else if(fog_f==3.0)
{ float x=1/exp(0.09*fog_d);fColor=mix(tex_color,fog_color,1-x);}
else if(fog_f==4.0)
{ float x=1/exp(0.09*0.09*fog_d*fog_d);fColor=mix(tex_color,fog_color,1-x);}
else
{ fColor =vec4(0,0,0,1);}

} 

