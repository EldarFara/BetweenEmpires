
attribute vec3 inPosition;

varying float2 texCoord0;
varying float2 texCoord1;
varying float2 texCoord2;
varying float2 texCoord3;

void main()
{
	gl_Position = vec4(inPosition, 1.0);

	// Texture coordinates
	float2 texCoord = (float2(inPosition.x, inPosition.y) * 0.5 + 0.5)/* + g_HalfPixel_ViewportSizeInv.xy*/;	

	texCoord0 = texCoord + float2(-1.0,  1.0) * g_HalfPixel_ViewportSizeInv.xy;
	texCoord1 = texCoord + float2( 1.0,  1.0) * g_HalfPixel_ViewportSizeInv.xy;
	texCoord2 = texCoord + float2( 1.0, -1.0) * g_HalfPixel_ViewportSizeInv.xy;
	texCoord3 = texCoord + float2(-1.0, -1.0) * g_HalfPixel_ViewportSizeInv.xy;
}
