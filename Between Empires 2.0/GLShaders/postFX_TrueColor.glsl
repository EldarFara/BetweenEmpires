
varying VS_OUT_POSTFX VSOut;

void main()
{
	const bool use_vignette = true;
	
	float4 ret = color_value;
	if(use_vignette)
	{
		ret.a = saturate(ret.a + ret.a * (1.0 - vignette(float2(texCoord.x * 2 - 1, texCoord.y * 2 - 1) * 0.5, 0.015, 1.25)) );	//remove blur from center
	}

	gl_FragColor = ret;
}
