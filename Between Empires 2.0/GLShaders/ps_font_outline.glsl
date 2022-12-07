
varying vec4 outColor0;
varying vec2 outTexCoord;



void main()
{ 
	float4 sample = texture2D(FontTextureSampler, outTexCoord);
	vec4 finalColor = outColor0;
	finalColor.a = (1.0 - sample.r) + sample.a;
	
	finalColor.rgb *= sample.a + 0.05;
	
	finalColor = saturate(finalColor);

	gl_FragColor = finalColor;
}