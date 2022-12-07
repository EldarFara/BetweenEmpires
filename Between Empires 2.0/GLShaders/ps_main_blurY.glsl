
varying float2 Tex;

void main()
{
	float BlurPixelWeight[8];
	BlurPixelWeight[0] = 0.256;
	BlurPixelWeight[1] = 0.240;
	BlurPixelWeight[2] = 0.144;
	BlurPixelWeight[3] = 0.135;
	BlurPixelWeight[4] = 0.120;
	BlurPixelWeight[5] = 0.065;
	BlurPixelWeight[6] = 0.030;
	BlurPixelWeight[7] = 0.010;
	
	float4 color = vec4(0.0);

	float2 BlurOffsetY = float2(0.0, g_HalfPixel_ViewportSizeInv.w);
	
	for(int i = 0; i < 8; i++)
	{
		color += texture2D(postFX_sampler0, Tex + (BlurOffsetY * float(i))) * BlurPixelWeight[i];
		color += texture2D(postFX_sampler0, Tex - (BlurOffsetY * float(i))) * BlurPixelWeight[i];
	}
	
	gl_FragColor = color;
}
