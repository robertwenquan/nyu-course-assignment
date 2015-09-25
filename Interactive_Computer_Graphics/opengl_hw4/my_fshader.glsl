in  vec4 color;
out vec4 fColor;
in float cur_y;

void main()
{
if(cur_y<0.1) discard;
fColor=color;
}