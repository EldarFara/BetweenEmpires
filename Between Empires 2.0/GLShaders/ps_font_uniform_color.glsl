
varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;



void main() 
{
	vec4 finalColor =  outColor0;
	finalColor.a *= texture2D(diffuse_texture, outTexCoord).a;
	gl_FragColor = finalColor;
}