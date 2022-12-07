
varying vec4 outColor0;
varying vec2 outTexCoord;

void main() 
{
	vec4 finalColor;
	finalColor.a = 1.0;
	finalColor.rgb = texture2D(FontTextureSampler, outTexCoord).rgb + outColor0.rgb;

	gl_FragColor = finalColor;
}