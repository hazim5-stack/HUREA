public protocol HureaWitnessFixtureProtocol { func fixtureValue() -> Int }
public struct HureaWitnessFixture: HureaWitnessFixtureProtocol {
  public init() {}
  public func fixtureValue() -> Int { 17 }
}
@_cdecl("hurea_witness_fixture_entry")
public func fixtureEntry() -> Int { HureaWitnessFixture().fixtureValue() }

public class HureaVtableFixture {
  public init() {}
  public func fixtureValue() -> Int { 23 }
}
