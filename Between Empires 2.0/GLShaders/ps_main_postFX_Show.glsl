
varying float2 Tex;

void main()
{
	float4 color = texture2D(postFX_sampler0, Tex);
	
	if(showing_ranged_data) 
	{
		color.rgb *= HDRRange;
		OUTPUT_GAMMA(color.rgb);
	}

	gl_FragColor = color;
}
