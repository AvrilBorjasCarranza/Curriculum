import { MeshGradient } from "@paper-design/shaders-react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Composition,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type Props = {};

const calculateMetadata: CalculateMetadataFunction<Props> = () => {
  return {};
};

export const MyComposition = () => {
  return (
    <Composition
      id="MyComp"
      component={MyComponent}
      durationInFrames={60}
      fps={30}
      width={1280}
      height={720}
      calculateMetadata={calculateMetadata}
    />
  );
};

// Test scene: Paper Shaders background driven by the Remotion frame (deterministic render).
export const MyComponent: React.FC<Props> = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <MeshGradient
        colors={["#5100ff", "#00ff80", "#ffcc00", "#ea00ff"]}
        distortion={1}
        swirl={0.8}
        speed={0}
        frame={(frame / fps) * 1000}
        style={{ width: "100%", height: "100%" }}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <h1 style={{ fontFamily: "sans-serif", fontSize: 96, color: "white", opacity }}>
          Remotion + Paper Shaders
        </h1>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
