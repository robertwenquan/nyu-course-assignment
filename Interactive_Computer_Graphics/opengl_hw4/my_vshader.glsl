in  vec3 velocity;
in  vec3 vColor;
out vec4 color;
out float cur_y;

uniform mat4 model_view;
uniform mat4 projection;
uniform float time;

void main() 
{
float tmp_a=time*velocity.x*0.001;
float tmp_b=0.1+0.001*velocity[1]*time+0.5*(-0.00000049)*time*time;
float tmp_c=velocity[2]*time*0.001;
cur_y=tmp_b;
vec4 vPosition4 = vec4(tmp_a, tmp_b, tmp_c, 1.0);
vec4 vColor4 = vec4(vColor.r, vColor.g, vColor.b, 1.0); 

    // YJC: Original, incorrect below:
    //      gl_Position = projection*model_view*vPosition/vPosition.w;

    gl_Position = projection * model_view * vPosition4;

    color = vColor4;
} 
