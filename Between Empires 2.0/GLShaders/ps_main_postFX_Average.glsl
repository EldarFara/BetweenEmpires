
varying float2 Tex;

void main()
{
	float Offsets[4];
	Offsets[0] = -1.5;
	Offsets[1] = -0.5;
	Offsets[2] = 0.5;
	Offsets[3] = 1.5;

	float _max = 0.0;
	float _log_sum = 0.0;
	
	for(int x = 0; x < 4; x++)
	{
		for(int y = 0; y < 4; y++)
		{
			float2 vOffset = float2(Offsets[x], Offsets[y]) * float2(g_HalfPixel_ViewportSizeInv.y, g_HalfPixel_ViewportSizeInv.w);
			float3 color_here = texture2D(postFX_sampler0, Tex + vOffset).rgb;
			float lum_here = dot(color_here * HDRRange, LUMINANCE_WEIGHTS);
			
			_log_sum += lum_here;
			_max = max(_max, lum_here);
		}
	}
	
	gl_FragColor = float4(_log_sum / 16.0, _max, 0.0, 1.0);
}
