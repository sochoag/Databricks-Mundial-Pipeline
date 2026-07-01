"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import { OrbitControls, Stars } from "@react-three/drei";
import * as THREE from "three";

// ISO alpha-2 codes of the 32 World Cup 2022 teams
const WC_COUNTRIES = new Set([
  "QA","EC","SN","NL","GB-ENG","IR","US","GB-WLS","AR","SA","MX","PL",
  "FR","AU","DK","TN","ES","CR","DE","JP","BE","CA","MA","HR","BR","RS",
  "CH","CM","PT","GH","UY","KR",
]);

// Approximate lat/lon for globe markers (country_code → [lat, lon])
const COUNTRY_COORDS: Record<string, [number, number]> = {
  QA:[25.3,51.2],EC:[-1.8,-78.2],SN:[14.5,-14.5],NL:[52.1,5.3],
  "GB-ENG":[52.4,-1.9],"GB-WLS":[52.1,-3.8],IR:[35.7,51.4],US:[38,-97],
  AR:[-34,-64],SA:[23.9,45.1],MX:[23.6,-102],PL:[51.9,19.1],
  FR:[46.2,2.2],AU:[-25.3,133.8],DK:[56.3,9.5],TN:[33.9,9.5],
  ES:[40.5,-3.7],CR:[9.7,-83.8],DE:[51.2,10.5],JP:[36.2,138.3],
  BE:[50.5,4.5],CA:[56.1,-106.3],MA:[31.8,-7.1],HR:[45.1,15.2],
  BR:[-14.2,-51.9],RS:[44.0,21.0],CH:[46.8,8.2],CM:[3.9,11.5],
  PT:[39.4,-8.2],GH:[7.9,-1.0],UY:[-32.5,-55.8],KR:[35.9,127.8],
};

function latLonToVec3(lat: number, lon: number, r: number): THREE.Vector3 {
  const phi = (90 - lat) * (Math.PI / 180);
  const theta = (lon + 180) * (Math.PI / 180);
  return new THREE.Vector3(
    -r * Math.sin(phi) * Math.cos(theta),
    r * Math.cos(phi),
    r * Math.sin(phi) * Math.sin(theta)
  );
}

function Markers({ onCountryClick }: { onCountryClick: (code: string) => void }) {
  return (
    <>
      {Object.entries(COUNTRY_COORDS).map(([code, [lat, lon]]) => {
        const pos = latLonToVec3(lat, lon, 1.02);
        return (
          <mesh
            key={code}
            position={pos}
            onClick={(e) => { e.stopPropagation(); onCountryClick(code); }}
          >
            <sphereGeometry args={[0.018, 8, 8]} />
            <meshStandardMaterial
              color="#34d399"
              emissive="#10b981"
              emissiveIntensity={0.8}
            />
          </mesh>
        );
      })}
    </>
  );
}

function Globe({ onCountryClick }: { onCountryClick: (code: string) => void }) {
  const ref = useRef<THREE.Mesh>(null!);

  useFrame((_, delta) => {
    ref.current.rotation.y += delta * 0.08;
  });

  return (
    <group>
      {/* Earth sphere */}
      <mesh ref={ref}>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial color="#1e3a5f" wireframe={false} />
      </mesh>
      {/* Wireframe overlay */}
      <mesh>
        <sphereGeometry args={[1.001, 32, 32]} />
        <meshStandardMaterial color="#334155" wireframe transparent opacity={0.3} />
      </mesh>
      {/* Country markers */}
      <Markers onCountryClick={onCountryClick} />
    </group>
  );
}

export default function GlobeScene({
  onCountryClick,
}: {
  onCountryClick: (code: string) => void;
}) {
  return (
    <Canvas camera={{ position: [0, 0, 2.8], fov: 45 }}>
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 3, 5]} intensity={1.2} />
      <pointLight position={[-5, -3, -5]} intensity={0.3} color="#60a5fa" />
      <Stars radius={100} depth={50} count={4000} factor={4} fade />
      <Globe onCountryClick={onCountryClick} />
      <OrbitControls
        enablePan={false}
        minDistance={1.8}
        maxDistance={4}
        autoRotate={false}
      />
    </Canvas>
  );
}
